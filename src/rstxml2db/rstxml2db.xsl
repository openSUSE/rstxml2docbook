<?xml version="1.0" encoding="UTF-8"?>
<!--
   Purpose:
     Transforms RST XML into DocBook

   Parameters:
     * indexfile
       Path to the '.booktree.xml' file

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

  <xsl:param name="xml.ext">.xml</xsl:param>
  <xsl:param name="indexfile" select="'.booktree.xml'"/>

  <xsl:variable name="index" select="document($indexfile, .)"/>
  <xsl:variable name="sections" select="$index//section"/>
  <xsl:variable name="indexids" select="$index//@id"/>

  <xsl:template match="*">
    <xsl:message>WARN: Unknown element '<xsl:value-of select="local-name()"/>'</xsl:message>
  </xsl:template>


  <xsl:template name="has.section.id">
    <xsl:param name="id"/>

    <xsl:value-of select="boolean($indexids[. = $id])"/>
  </xsl:template>

  <xsl:template name="get.section.from.id">
    <xsl:param name="id"/>

    <xsl:value-of select="$sections[@id = $id]"/>
  </xsl:template>

  <xsl:template name="get.level.from.id">
    <xsl:param name="id"/>

    <xsl:value-of select="$index//*[@id = $id]/@level"/>
  </xsl:template>

  <xsl:template name="get.structural.name">
    <xsl:param name="level"/>
    <xsl:choose>
      <xsl:when test="$level = 0">book</xsl:when>
      <xsl:when test="$level = 1">chapter</xsl:when>
      <xsl:when test="$level = 2">sect1</xsl:when>
      <xsl:when test="$level = 3">sect2</xsl:when>
      <xsl:when test="$level = 4">sect3</xsl:when>
      <xsl:when test="$level = 5">sect4</xsl:when>
      <xsl:when test="$level = 6">sect5</xsl:when>
      <xsl:otherwise>
        <xsl:message>ERROR: Level too big!</xsl:message>
        <xsl:text>topic</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="create.structural.name">
    <xsl:param name="id" select="@ids"/>
    <xsl:variable name="level">
      <xsl:call-template name="get.level.from.id">
        <xsl:with-param name="id" select="$id"/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="name">
      <xsl:call-template name="get.structural.name">
        <xsl:with-param name="level" select="$level"/>
      </xsl:call-template>
    </xsl:variable>

    <xsl:value-of select="$name"/>
  </xsl:template>

  <xsl:template name="get.target.id">
    <xsl:param name="node" select="."/>

    <xsl:choose>
        <xsl:when test="$node/preceding-sibling::section[1]/section[1]/section[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::section[1]/section[1]/section[1]/*[last()][self::target]/@refid"/>
        </xsl:when>
        <xsl:when test="$node/preceding-sibling::section[1]/section[1]/*[last()][self::target]">
          <xsl:value-of select="$node/preceding-sibling::section[1]/section[1]/*[last()][self::target]/@refid"/>
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

  <!-- =================================================================== -->
  <!-- Ignored elements                                                    -->
  <xsl:template match="section[@names='search\ in\ this\ guide']"/>

  <xsl:template match="comment"/>
  <xsl:template match="index"/>
  <xsl:template match="target"/>
  <xsl:template match="substitution_definition"/>


  <!-- =================================================================== -->
  <xsl:template match="document">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="section[@names='abstract']">
    <xsl:param name="root"/>
    <xsl:element name="{$root}info">
      <abstract>
        <xsl:apply-templates/>
      </abstract>
    </xsl:element>
  </xsl:template>

  <xsl:template match="section">
    <xsl:variable name="name">
      <xsl:call-template name="create.structural.name"/>
    </xsl:variable>
    <xsl:variable name="idattr">
      <xsl:call-template name="get.target.id"/>
    </xsl:variable>

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

  <xsl:template match="bullet_list[@bullet='-' or @bullet='*']">
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
    <step>
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
  <xsl:template match="glossary">
    <!--<glossary>
      <xsl:copy-of select="ancestor::title"/>-->
      <xsl:apply-templates/>
    <!--</glossary>-->
  </xsl:template>

  <xsl:template match="definition_list[@classes='glossary']">
    <glosslist>
      <xsl:apply-templates select="definition_list_item"/>
    </glosslist>
  </xsl:template>

  <xsl:template match="definition_list[@classes='glossary']/definition_list_item">
    <glossentry>
      <xsl:apply-templates/>
    </glossentry>
  </xsl:template>

  <xsl:template match="definition_list[@classes='glossary']/definition_list_item/term">
    <glossterm>
      <xsl:apply-templates/>
    </glossterm>
  </xsl:template>

  <xsl:template match="definition_list[@classes='glossary']/definition_list_item/definition">
    <glossdef>
      <xsl:apply-templates/>
    </glossdef>
  </xsl:template>


  <!-- =================================================================== -->
  <xsl:template match="table">
    <informaltable>
      <xsl:apply-templates mode="table"/>
    </informaltable>
  </xsl:template>

  <xsl:template match="@stub" mode="table"/>

  <xsl:template match="node() | @*" mode="table">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()" mode="table"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="colspec" mode="table">
    <colspec>
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

  <!-- =================================================================== -->
  <xsl:template match="figure">
    <figure>
      <xsl:choose>
        <xsl:when test="following-sibling::paragraph[strong]">
          <xsl:variable name="title">
            <xsl:value-of select="substring-after('Figure', following-sibling::paragraph[1]/strong)"/>
          </xsl:variable>
          <title><xsl:value-of select="$title"/></title>
        </xsl:when>
        <xsl:when test="caption">
          <title>
            <xsl:apply-templates select="caption"/>
          </title>
        </xsl:when>
      </xsl:choose>
      <xsl:apply-templates select="node()[not(self::caption)]"/>
    </figure>
  </xsl:template>

  <xsl:template match="caption|caption/strong">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="image">
    <xsl:variable name="uri" select="@uri"/>
    <mediaobject>
      <imageobject role="fo">
        <imagedata fileref="{$uri}" width="{@width}"/>
      </imageobject>
      <imageobject role="html">
        <imagedata fileref="{$uri}" width="{@width}"/>
      </imageobject>
    </mediaobject>
  </xsl:template>

  <xsl:template match="paragraph[strong][preceding-sibling::figure]"/>


  <!-- =================================================================== -->
  <xsl:template match="emphasis">
    <xsl:copy-of select="."/>
  </xsl:template>

  <xsl:template match="emphasis[@classes='guilabel']">
    <guilabel>
      <xsl:apply-templates/>
    </guilabel>
  </xsl:template>

  <xsl:template match="emphasis[@classes='menuselection']">
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

  <xsl:template match="strong[@classes='command']">
    <command>
      <xsl:apply-templates/>
    </command>
  </xsl:template>

  <xsl:template match="strong">
    <emphasis role="bold">
      <xsl:apply-templates/>
    </emphasis>
  </xsl:template>

  <xsl:template match="literal">
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

  <xsl:template match="reference[@refid]">
    <xref linkend="{@refid}"/>
  </xsl:template>

  <xsl:template match="title_reference">
    <literal>
      <xsl:apply-templates/>
    </literal>
  </xsl:template>

</xsl:stylesheet>