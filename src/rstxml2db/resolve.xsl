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
  
  <!-- ================================================================== -->
  <xsl:param name="xml.ext">.xml</xsl:param>
  <xsl:param name="root.role">big</xsl:param>


  <!-- ================================================================== -->
  <xsl:template name="getdir">
   <xsl:param name="filename" select="''"/>
   <xsl:if test="contains($filename, '/')">
    <xsl:value-of select="substring-before($filename, '/')"/>
    <xsl:text>/</xsl:text>
    <xsl:call-template name="getdir">
     <xsl:with-param name="filename" select="substring-after($filename, '/')"/>
    </xsl:call-template>
   </xsl:if>
  </xsl:template>

  <!-- ================================================================== -->
  <xsl:template match="node() | @*">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>


  <!-- ================================================================== -->
  <xsl:variable name="basepath">
   <xsl:call-template name="getdir">
    <xsl:with-param name="filename" select="/document/@source"/>
   </xsl:call-template>
  </xsl:variable>

  <!-- ================================================================== -->
  <xsl:template match="/document">
    <xsl:param name="xmlbase"/>
    <document role="{$root.role}" xml:base="{$xmlbase}">
     <xsl:attribute name="relsource">
      <xsl:value-of select="substring-after(@source, $basepath)"/>
     </xsl:attribute>
      <xsl:copy-of select="@*"/>
      <xsl:apply-templates>
        <xsl:with-param name="role" select="''"/>
      </xsl:apply-templates>
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
    <xsl:variable name="ref" select="concat($refuri, $xml.ext)"/>
    <xsl:message>INFO: Including "<xsl:value-of select="$ref"/>"...</xsl:message>
    <xsl:apply-templates select="document($ref, .)">
      <xsl:with-param name="role" select="''"/>
      <xsl:with-param name="xmlbase" select="$refuri"/>
    </xsl:apply-templates>
  </xsl:template>

</xsl:stylesheet>