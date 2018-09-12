<?xml version="1.0" encoding="UTF-8"?>
<!--
   Purpose:
     "Resolves" RST XML index.xml file into one, single RST XML file

   Parameters:
     * xml.ext (default '.xml')
       Parameter will be appended to be read in by the document() function

   Input:
     RST XML file, converted with sphinx-build using option -b xml
     Usually you should use 'index.xml' to start with

   Output:
     Single RST XML file without any toctree-wrapper or content sections

   Author:
     Thomas Schraitle <toms AT opensuse.org>
     Copyright 2016 SUSE Linux GmbH

-->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common"
  exclude-result-prefixes="exsl">

  <xsl:key name="id" match="*" use="@ids"/>

  <!-- ================================================================== -->
  <xsl:param name="xml.ext">.xml</xsl:param>
  <xsl:param name="root.role">big</xsl:param>
  
  <!-- ================================================================== -->
  <xsl:template match="node() | @*">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- ================================================================== -->
  <xsl:template match="/document">
    <xsl:param name="xmlbase"/>
    <xsl:param name="anchor"/>
    <xsl:variable name="root.element" select="key('id', $anchor)"/>

    <document role="{$root.role}" xml:base="{$xmlbase}">
      <xsl:copy-of select="@*"/>
      <xsl:choose>
       <xsl:when test="count($root.element) = 0">
        <xsl:apply-templates>
         <xsl:with-param name="role" select="''"/>
        </xsl:apply-templates>
       </xsl:when>
       <xsl:otherwise>
        <xsl:attribute name="role">part</xsl:attribute>
        <xsl:apply-templates select="$root.element">
         <xsl:with-param name="role" select="''"/>
        </xsl:apply-templates>
       </xsl:otherwise>
      </xsl:choose>
    </document>
  </xsl:template>

  <xsl:template match="section[@names='contents']">
    <xsl:apply-templates mode="xinclude"/>
  </xsl:template>

  <xsl:template match="compound[@classes='toctree-wrapper']">
    <xsl:apply-templates mode="xinclude"/>
  </xsl:template>

  <xsl:template match="text()" mode="xinclude"/>

  <xsl:template match="list_item[@classes='toctree-l1']" mode="xinclude">
    <xsl:variable name="refuri" select="*/reference/@refuri"/>
    <xsl:variable name="anchor" select="substring-after($refuri, '#')"/>
    <xsl:variable name="ref">
     <xsl:choose>
      <xsl:when test="$anchor">
       <xsl:value-of select="concat(substring-before($refuri, '#'), $xml.ext)"/>
      </xsl:when>
      <xsl:otherwise>
       <xsl:value-of select="concat($refuri, $xml.ext)"/>
      </xsl:otherwise>
     </xsl:choose>
    </xsl:variable>

    <xsl:message>INFO: Including "<xsl:value-of select="$ref"/>"<xsl:if test="$anchor"
     > with anchor '<xsl:value-of select="$anchor"/>'</xsl:if>...</xsl:message>
    <xsl:apply-templates select="document($ref, .)">
      <xsl:with-param name="role" select="''"/>
      <xsl:with-param name="anchor" select="$anchor"/>
      <xsl:with-param name="xmlbase" select="$refuri"/>
    </xsl:apply-templates>
  </xsl:template>

</xsl:stylesheet>