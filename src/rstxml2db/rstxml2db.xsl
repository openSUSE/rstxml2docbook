<?xml version="1.0" encoding="UTF-8"?>
<!--
   Purpose:
     Transforms RST XML into DocBook

   Parameters:
     * productname
       The name of the product; added inside <bookinfo>
     * produtnumber
       The number or any other identification of a product; added inside
       <bookinfo>
     * xml.ext
       References to XML files; this parameter contains the extension
       (usually '.xml') which is appended for the reference/@refuri part.
     * rootlang
       (Natural) language of the document; added into the root element as
       lang="$rootlang"

   Input:
     RST XML file, converted with sphinx-build using option -b xml

   Output:
     DocBook 4 document

   Author:
     Thomas Schraitle <toms AT opensuse.org>
     Copyright 2016 SUSE Linux GmbH

-->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common"
  exclude-result-prefixes="exsl">

  <xsl:output indent="yes"/>
  <xsl:strip-space elements="*"/>

  <xsl:key name="id" match="*" use="@ids"/>
  <xsl:key name="documents" match="document" use="@source"/>

  <xsl:param name="xml.ext">.xml</xsl:param>

  <!-- Natural language for root element -->
  <xsl:param name="rootlang">en</xsl:param>

  <xsl:param name="productname"/>
  <xsl:param name="productnumber"/>


  <xsl:template match="*">
    <xsl:message>WARN: Unknown element '<xsl:value-of select="local-name()"/>'</xsl:message>
  </xsl:template>


  <xsl:template name="get.structural.name">
    <xsl:param name="level"/>
    <xsl:choose>
      <xsl:when test="$level = 0">book</xsl:when>
      <xsl:when test="$level = 1">chapter</xsl:when>
      <xsl:when test="$level >= 2">section</xsl:when>
      <!--
      <xsl:when test="$level = 3">sect2</xsl:when>
      <xsl:when test="$level = 4">sect3</xsl:when>
      <xsl:when test="$level = 5">sect4</xsl:when>
      <xsl:when test="$level = 6">sect5</xsl:when>
      -->
      <xsl:otherwise>
        <xsl:message>ERROR: Level out of scope (level=<xsl:value-of select="$level"/>)</xsl:message>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="create.structural.name">
    <xsl:param name="id" select="@ids"/>
    <xsl:variable name="level" select="count(ancestor::section)"/>
    <xsl:variable name="name">
      <xsl:call-template name="get.structural.name">
        <xsl:with-param name="level" select="$level"/>
      </xsl:call-template>
    </xsl:variable>

    <xsl:value-of select="$name"/>
  </xsl:template>

  <xsl:template name="get.target4section.id">
    <xsl:param name="node" select="."/>

    <xsl:choose>
       <xsl:when test="not(contains($node/@ids, ' '))">
         <xsl:value-of select="$node/@ids"/>
       </xsl:when>
        <xsl:when test="$node/preceding-sibling::section[1]/section[1]/section[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::section[1]/section[1]/section[1]/*[last()][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="$node/preceding-sibling::section[1]/section[last()]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::section[1]/section[last()]/*[last()][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="$node/preceding-sibling::section[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::section[1]/*[last()][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="$node/preceding-sibling::*[1][self::target]">
          <xsl:value-of select="$node/preceding-sibling::*[1][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="contains($node/@ids, ' ')">
          <xsl:value-of select="substring-after($node/@ids, ' ')"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$node/@ids"/>
        </xsl:otherwise>
      </xsl:choose>
  </xsl:template>

  <xsl:template name="get.target4table.id">
    <xsl:param name="node" select="."/>

    <xsl:choose>
        <!--<xsl:when test="$node/preceding-sibling::section[1]/section[1]/section[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::section[1]/section[1]/section[1]/*[last()][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="$node/preceding-sibling::section[1]/section[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::section[1]/section[1]/*[last()][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="$node/preceding-sibling::section[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::section[1]/*[last()][self::target]/@refid"/>
        </xsl:when>-->
        <xsl:when test="$node/preceding-sibling::*[2][self::target]">
          <xsl:value-of select="$node/preceding-sibling::*[2][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="$node/preceding-sibling::*[1][self::target]">
          <xsl:value-of select="$node/preceding-sibling::*[1][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="contains($node/@ids, ' ')">
          <xsl:value-of select="substring-after($node/@ids, ' ')"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$node/@ids"/>
        </xsl:otherwise>
      </xsl:choose>
  </xsl:template>

  <xsl:template name="get.target.id">
    <xsl:param name="node" select="."/>

    <xsl:choose>
        <!--<xsl:when test="$node/preceding-sibling::*[1]/*[1]/*[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::*[1]/*[1]/*[1]/*[last()][self::target]/@refid"/>
        </xsl:when>-->
        <!--<xsl:when test="$node/preceding-sibling::*[1]/*[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::*[1]/*[1]/*[last()][self::target]/@refid"/>
        </xsl:when>-->
        <xsl:when test="$node/preceding-sibling::*[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::*[1]/*[last()][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="$node/preceding-sibling::*[1][self::target]">
          <xsl:value-of select="$node/preceding-sibling::*[1][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="contains($node/@ids, ' ')">
          <xsl:value-of select="substring-after($node/@ids, ' ')"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$node/@ids"/>
        </xsl:otherwise>
      </xsl:choose>
  </xsl:template>

  <!-- Taken from common/common.xsl of the DocBook stylesheets -->
  <xsl:template name="filename-basename">
    <!-- We assume all filenames are really URIs and use "/" -->
    <xsl:param name="filename"/>
    <xsl:param name="recurse" select="false()"/>

    <xsl:choose>
      <xsl:when test="substring-after($filename, '/') != ''">
        <xsl:call-template name="filename-basename">
          <xsl:with-param name="filename" select="substring-after($filename, '/')"/>
          <xsl:with-param name="recurse" select="true()"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$filename"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- =================================================================== -->
  <!-- Ignored elements                                                    -->
  <xsl:template match="section[@names='search\ in\ this\ guide']"/>
  <xsl:template match="section[@names='abstract']"/>

  <xsl:template match="comment"/>
  <xsl:template match="index"/>
  <xsl:template match="target"/>
  <xsl:template match="substitution_definition"/>

  <!-- =================================================================== -->
  <!-- Skipped elements                                                    -->
  <xsl:template match="hlist|hlistcol">
   <xsl:apply-templates/>
  </xsl:template>

  <!-- =================================================================== -->
  <xsl:template match="document">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="/document[@role='big']/section">
    <xsl:variable name="idattr">
      <xsl:call-template name="get.target4section.id"/>
    </xsl:variable>

    <book lang="{$rootlang}">
      <xsl:if test="$idattr != ''">
        <xsl:attribute name="id">
          <xsl:value-of select="$idattr"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates select="title"/>
      <bookinfo>
        <xsl:apply-templates select="section[@names='abstract']" mode="bookinfo"/>
        <xsl:if test="$productname != ''">
          <productname>
            <xsl:value-of select="$productname"/>
          </productname>
        </xsl:if>
        <xsl:if test="$productnumber != ''">
          <productnumber>
            <xsl:value-of select="$productnumber"/>
          </productnumber>
        </xsl:if>
      </bookinfo>
      <xsl:apply-templates select="*[not(self::title)]"/>
    </book>
  </xsl:template>

  <xsl:template match="/document[@role='big']/section/document/section">
    <xsl:variable name="idattr">
      <xsl:call-template name="get.target4section.id"/>
    </xsl:variable>

    <chapter>
      <xsl:if test="$idattr != ''">
        <xsl:attribute name="id">
          <xsl:value-of select="$idattr"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </chapter>
  </xsl:template>

  <xsl:template match="section[@names = 'abstract']" mode="bookinfo">
     <abstract>
      <xsl:apply-templates/>
    </abstract>
  </xsl:template>

  <xsl:template match="section">
    <xsl:variable name="name">
      <xsl:call-template name="create.structural.name"/>
    </xsl:variable>
    <xsl:variable name="idattr">
      <xsl:call-template name="get.target4section.id"/>
    </xsl:variable>
    <xsl:variable name="level" select="count(ancestor::section)"/>

    <xsl:element name="{$name}">
      <xsl:if test="@ids">
        <xsl:attribute name="id">
          <xsl:value-of select="$idattr"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates>
        <xsl:with-param name="root" select="$name"/>
      </xsl:apply-templates>
    </xsl:element>
  </xsl:template>

  <xsl:template match="section/title">
    <title>
      <xsl:apply-templates/>
    </title>
  </xsl:template>

  <xsl:template match="section[@names='contents']">
    <xsl:apply-templates mode="xinclude"/>
  </xsl:template>

  <xsl:template match="compound[@classes='toctree-wrapper']">
    <xsl:apply-templates mode="xinclude"/>
  </xsl:template>

  <xsl:template match="text()" mode="xinclude"/>

  <xsl:template match="list_item[@classes='toctree-l1']" mode="xinclude">
    <xsl:variable name="xiref" select="concat(*/reference/@refuri, $xml.ext)"/>
    <!--<xi:include href="{$xiref}" xmlns:xi="http://www.w3.org/2001/XInclude"/>-->
    <xsl:element name="xi:include" namespace="http://www.w3.org/2001/XInclude">
      <xsl:attribute name="href">
        <xsl:value-of select="$xiref"/>
      </xsl:attribute>
    </xsl:element>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>


  <!-- =================================================================== -->
  <xsl:template match="block_quote">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="literal_block[@language='shell' or @language='console']">
    <screen>
      <xsl:apply-templates/>
    </screen>
  </xsl:template>

  <xsl:template match="literal_block[@language]|block_quote/literal_block[@language]">
    <screen language="{@language}">
      <xsl:apply-templates/>
    </screen>
  </xsl:template>

  <xsl:template match="line_block[line[normalize-space(.)='']]"/>

  <xsl:template match="literal_block">
    <screen>
      <xsl:apply-templates/>
    </screen>
  </xsl:template>

  <xsl:template match="note|tip|warning|caution|important">
    <xsl:variable name="name">
      <xsl:choose>
        <xsl:when test="local-name()='caution'">important</xsl:when>
        <xsl:otherwise><xsl:value-of select="local-name(.)"/></xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:element name="{$name}">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="paragraph">
    <para>
      <xsl:apply-templates/>
    </para>
  </xsl:template>

  <xsl:template match="bullet_list[@bullet='-' or @bullet='*']|bullet_list">
    <itemizedlist>
      <xsl:apply-templates/>
    </itemizedlist>
  </xsl:template>

  <xsl:template match="list_item">
    <listitem>
      <xsl:apply-templates/>
    </listitem>
  </xsl:template>

  <xsl:template match="enumerated_list">
    <procedure>
      <xsl:apply-templates/>
    </procedure>
  </xsl:template>

  <xsl:template match="enumerated_list/list_item">
    <xsl:variable name="id">
      <xsl:call-template name="get.target.id"/>
    </xsl:variable>
    <step>
      <xsl:if test="$id != ''">
        <xsl:attribute name="id"><xsl:value-of select="$id"/></xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </step>
  </xsl:template>

  <xsl:template match="definition_list">
    <variablelist>
      <xsl:apply-templates select="definition_list_item"/>
    </variablelist>
  </xsl:template>

  <xsl:template match="definition_list_item">
    <varlistentry>
      <xsl:apply-templates/>
      <xsl:apply-templates select="../definition"/>
    </varlistentry>
  </xsl:template>

  <xsl:template match="definition_list_item/term">
    <term>
      <xsl:apply-templates/>
    </term>
  </xsl:template>

  <xsl:template match="definition">
    <listitem>
      <xsl:apply-templates/>
    </listitem>
  </xsl:template>


  <!-- =================================================================== -->
  <xsl:template match="section[@names='glossary'][document/section[@names='glossary']]">
   <!-- Just skip this double entry: -->
   <xsl:message>INFO: skipping document for glossary</xsl:message>
   <xsl:apply-templates select="document/section[@names='glossary']"/>
  </xsl:template>

  <xsl:template match="document/section[@names='glossary']">
   <glossary>
    <xsl:apply-templates/>
   </glossary>
  </xsl:template>

 <xsl:template match="section[@names='glossary']/section">
  <xsl:variable name="name">
   <xsl:call-template name="create.structural.name"/>
  </xsl:variable>
  <xsl:variable name="idattr">
   <xsl:call-template name="get.target4section.id"/>
  </xsl:variable>
  <xsl:message>INFO: Add glossdiv <xsl:value-of select="$idattr"/></xsl:message>
  <glossdiv id="{$idattr}">
   <xsl:apply-templates select="title"/>
   <xsl:apply-templates select="*[not(self::title)]"/>
  </glossdiv>
 </xsl:template>

 <xsl:template match="section[@names='glossary']/section/glossary">
  <xsl:apply-templates/>
 </xsl:template>

  <xsl:template match="*" mode="glossary">
      <xsl:apply-templates select="."/>
  </xsl:template>

  <xsl:template match="glossary">
      <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="definition_list[@classes='glossary']">
      <xsl:apply-templates select="definition_list_item"/>
  </xsl:template>

  <xsl:template match="definition_list[@classes='glossary']/definition_list_item">
   <xsl:variable name="idattr">
     <xsl:value-of select="term/@ids"/>
   </xsl:variable>
    <glossentry>
      <xsl:if test="$idattr">
        <xsl:attribute name="id">
          <xsl:value-of select="$idattr"/>
        </xsl:attribute>
        <xsl:message>INFO: Add id=<xsl:value-of select="$idattr"/></xsl:message>
      </xsl:if>
      <xsl:apply-templates select="term"/>
      <xsl:apply-templates select="definition"/>
    </glossentry>
  </xsl:template>

  <xsl:template match="definition_list[@classes='glossary']/definition_list_item/term">
   <glossterm>
      <xsl:apply-templates/>
   </glossterm>
  </xsl:template>

  <xsl:template match="definition_list[@classes='glossary']/definition_list_item/term/index"/>

  <xsl:template match="definition_list[@classes='glossary']/definition_list_item/definition">
    <xsl:message>INFO: Add definition of <xsl:value-of select="normalize-space(../term)"/>, id=<xsl:value-of select="../term/@ids"/></xsl:message>
    <glossdef>
      <xsl:apply-templates/>
    </glossdef>
  </xsl:template>


  <!-- =================================================================== -->
  <xsl:template match="table">
    <xsl:variable name="title">
     <xsl:choose>
      <xsl:when test="title">
       <xsl:apply-templates select="title"/>
      </xsl:when>
      <!--<xsl:when test="preceding-sibling::paragraph[1][strong]">
       <xsl:apply-templates select="preceding-sibling::paragraph[1]/strong"/>
      </xsl:when>-->
     </xsl:choose>
    </xsl:variable>
    <xsl:variable name="id">
      <xsl:call-template name="get.target4table.id"/>
    </xsl:variable>
    <xsl:variable name="tabletype">
      <xsl:choose>
        <xsl:when test="$title != ''">table</xsl:when>
        <xsl:otherwise>informaltable</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

<!--    <xsl:message>table:
    title=<xsl:value-of select="$title"/>
    id=<xsl:value-of select="$id"/>
    type=<xsl:value-of select="$tabletype"/>
    </xsl:message>-->

    <xsl:element name="{$tabletype}">
      <xsl:if test="$id != ''">
        <xsl:attribute name="id">
          <xsl:value-of select="$id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="$title != '' and $tabletype = 'table'">
        <xsl:copy-of select="$title"/>
      </xsl:if>
      <xsl:apply-templates mode="table"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="table/title">
   <xsl:variable name="content">
    <xsl:apply-templates/>
   </xsl:variable>
   <title><xsl:value-of select="normalize-space($content)"/></title>
  </xsl:template>

  <xsl:template match="@stub" mode="table"/>

  <xsl:template match="@morecols" mode="table">
   <xsl:attribute name="namest">c1</xsl:attribute>
   <xsl:attribute name="nameend">
    <xsl:text>c</xsl:text>
    <xsl:value-of select=". +1"/>
   </xsl:attribute>
  </xsl:template>

  <xsl:template match="node() | @*" mode="table">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()" mode="table"/>
    </xsl:copy>
  </xsl:template>
 
 <xsl:template match="title" mode="table"/>

  <xsl:template match="colspec" mode="table">
    <colspec colname="c{position() -1}">
      <xsl:apply-templates select="@*" mode="table"/>
    </colspec>
  </xsl:template>


  <xsl:template match="paragraph" mode="table">
    <para>
      <xsl:apply-templates/>
    </para>
  </xsl:template>

  <xsl:template match="literal_block|definition_list|bullet_list" mode="table">
    <xsl:apply-templates select="."/>
  </xsl:template>

  <xsl:template match="option_list">
   <variablelist>
    <xsl:apply-templates/>
   </variablelist>
  </xsl:template>

  <xsl:template match="option_list_item">
   <varlistentry>
    <xsl:apply-templates/>
   </varlistentry>
  </xsl:template>

  <xsl:template match="option_group">
   <term>
    <xsl:apply-templates/>
   </term>
  </xsl:template>

  <xsl:template match="option">
   <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="option_string">
   <option><xsl:apply-templates/></option>
  </xsl:template>

  <xsl:template match="description">
   <listitem>
    <xsl:apply-templates/>
   </listitem>
  </xsl:template>


  <!-- =================================================================== -->
  <xsl:template match="figure">
    <xsl:variable name="title">
      <xsl:choose>
        <xsl:when test="following-sibling::paragraph[1][strong]">
          <xsl:variable name="tmp.title" select="following-sibling::paragraph[1][strong]"/>
          <xsl:choose>
            <xsl:when test="starts-with($tmp.title, 'Figure:&#xa0;')">
              <xsl:value-of select="substring-after($tmp.title, 'Figure:&#xa0;')"/>
            </xsl:when>
            <xsl:when test="starts-with($tmp.title, 'Figure&#xa0;')">
              <xsl:value-of select="substring-after($tmp.title, 'Figure&#xa0;')"/>
            </xsl:when>
            <xsl:when test="starts-with($tmp.title, 'Figure:')">
              <xsl:value-of select="substring-after($tmp.title, 'Figure:')"/>
            </xsl:when>
            <xsl:when test="starts-with($tmp.title, 'Figure')">
              <xsl:value-of select="substring-after($tmp.title, 'Figure')"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="$tmp.title"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:when>
        <xsl:otherwise>
          <xsl:apply-templates select="caption"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <figure>
      <title><xsl:value-of select="normalize-space($title)"/></title>
      <xsl:apply-templates select="node()[not(self::caption)]"/>
    </figure>
  </xsl:template>

  <xsl:template match="caption|caption/strong">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="image">
    <xsl:variable name="uri">
      <xsl:call-template name="filename-basename">
        <xsl:with-param name="filename" select="@uri"></xsl:with-param>
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="imagedata">
     <imagedata fileref="{$uri}">
      <xsl:if test="@width">
       <xsl:attribute name="width">
        <xsl:value-of select="@width"/>
       </xsl:attribute>
      </xsl:if>
     </imagedata>
    </xsl:variable>
    <informalfigure>
     <mediaobject>
      <imageobject role="fo">
       <xsl:copy-of select="$imagedata"/>
      </imageobject>
      <imageobject role="html">
       <xsl:copy-of select="$imagedata"/>
      </imageobject>
     </mediaobject>
    </informalfigure>
  </xsl:template>

  <xsl:template match="paragraph[strong][preceding-sibling::figure]"/>


  <!-- =================================================================== -->
  <xsl:template match="emphasis">
    <xsl:copy-of select="."/>
  </xsl:template>

  <xsl:template match="inline">
   <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="emphasis[@classes='guilabel']|inline[@classes='guilabel']">
    <guilabel>
      <xsl:apply-templates/>
    </guilabel>
  </xsl:template>

  <xsl:template match="emphasis[@classes='menuselection']|inline[@classes='menuselection']">
    <menuchoice>
      <xsl:call-template name="create.guimenu">
        <xsl:with-param name="text" select="text()"/>
      </xsl:call-template>
    </menuchoice>
  </xsl:template>

  <xsl:template name="create.guimenu">
    <xsl:param name="text"/>
    <xsl:param name="delimiter">&gt;</xsl:param>

    <xsl:if test="$text != ''">
      <guimenu>
        <xsl:value-of select="normalize-space(substring-before(concat($text,$delimiter),$delimiter))"/>
      </guimenu>
      <xsl:call-template name="create.guimenu">
        <xsl:with-param name="text" select="substring-after($text, $delimiter)"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template match="strong[@classes='command']|literal_strong[@classes='command']">
    <command>
      <xsl:apply-templates/>
    </command>
  </xsl:template>

  <xsl:template match="strong">
    <emphasis role="bold">
      <xsl:apply-templates/>
    </emphasis>
  </xsl:template>

  <xsl:template match="literal|literal_strong">
    <literal>
      <xsl:apply-templates/>
    </literal>
  </xsl:template>

  <xsl:template match="literal_emphasis[contains(@classes, 'option')]">
    <option>
      <xsl:apply-templates/>
    </option>
  </xsl:template>

  <xsl:template match="reference[@refuri]">
    <ulink url="{@refuri}">
      <xsl:value-of select="."/>
    </ulink>
  </xsl:template>

  <xsl:template match="reference[@refuri][@internal='True']">
    <xsl:variable name="uri" select="substring-after(@refuri, '#')"/>

    <xsl:choose>
      <xsl:when test="$uri != ''">
        <xref linkend="{$uri}"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:variable name="refuri" select="concat(@refuri, '.xml')"/>
<!--        <xsl:variable name="sectid" select="($refs[@href=$refuri])[1]/section[1]/@id"/> -->
        <xsl:variable name="sectid" select="key('documents', @refuri)"/>
        <xsl:choose>
          <xsl:when test="$sectid != ''">
            <xref linkend="{$sectid}"/>
          </xsl:when>
          <xsl:otherwise>
            <!-- common/cli_set_environment_variables_using_openstack_rc.xml
              concat(@refuri, '.xml')
             -->
            <xsl:message>WARNING: could not find referenced ID '<xsl:value-of select="@refuri"/>'!
             sectid="<xsl:value-of select="$sectid"/>"
             refuri=<xsl:value-of select="$refuri"/>
             <!-- ref section=<xsl:value-of select="$refs[@href='common/cli_set_environment_variables_using_openstack_rc.xml']/section[1]/@id"/>--></xsl:message>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="reference[@refid]">
    <xref linkend="{@refid}"/>
  </xsl:template>

  <xsl:template match="title_reference">
    <literal>
      <xsl:apply-templates/>
    </literal>
  </xsl:template>

</xsl:stylesheet>