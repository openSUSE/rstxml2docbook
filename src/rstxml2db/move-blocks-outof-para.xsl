<?xml version="1.0" encoding="UTF-8"?>
<!--
   Purpose:
     Moves block elements inside <paragraphs> outside of <paragraphs>.

   Parameters:
     None

   Input:
     RST XML file, converted with sphinx-build using option -b xml

   Output:
     RST XML file

   Example:
     See https://github.com/openSUSE/rstxml2docbook/issues/76

   Author:
     Thomas Schraitle <toms AT opensuse.org>
     Copyright 2018 SUSE Linux GmbH

-->
<!DOCTYPE xsl:stylesheet
[
 <!ENTITY dbselfblocks "self::admonition |
                        self::attention |
                        self::block_quote |
                        self::bullet_list |
                        self::caution |
                        self::danger |
                        self::definition_list |
                        self::doctest_block |
                        self::enumerated_list |
                        self::error |
                        self::field_list |
                        self::figure |
                        self::hint |
                        self::important |
                        self::line_block |
                        self::literal_block |
                        self::math_block |
                        self::note |
                        self::option_list |
                        self::warning">
 <!ENTITY dbblocksinpara "paragraph/admonition |
                          paragraph/attention |
                          paragraph/block_quote |
                          paragraph/bullet_list |
                          paragraph/caution |
                          paragraph/danger |
                          paragraph/definition_list |
                          paragraph/doctest_block |
                          paragraph/enumerated_list |
                          paragraph/error |
                          paragraph/field_list |
                          paragraph/figure |
                          paragraph/hint |
                          paragraph/important |
                          paragraph/line_block |
                          paragraph/literal_block |
                          paragraph/math_block |
                          paragraph/note |
                          paragraph/option_list |
                          paragraph/warning">
]>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exsl="http://exslt.org/common" exclude-result-prefixes="exsl">

 <xsl:strip-space elements="paragraph"/>
 <xsl:preserve-space elements="literal_block"/>
 <xsl:output indent="yes"/>

 <!-- copy template==================================================== -->
 <xsl:template match="node() | @*">
  <xsl:copy>
   <xsl:apply-templates select="@* | node()"/>
  </xsl:copy>
 </xsl:template>


 <!-- Templates ======================================================= -->
 <xsl:template match="paragraph">
  <xsl:apply-templates select="node()[1]"/>
 </xsl:template>

 <xsl:template match="&dbblocksinpara;">
  <xsl:copy-of select="."/>
  <xsl:text>&#10;</xsl:text>
  <xsl:apply-templates select="following-sibling::node()[1]"/>
 </xsl:template>
 
 <xsl:template match="paragraph/*|paragraph/text()">
  <xsl:element name="{local-name(..)}">
   <xsl:apply-templates select="." mode="copy"/>
  </xsl:element>
  <xsl:text>&#10;</xsl:text>
  <xsl:apply-templates
   select="following-sibling::*[&dbselfblocks;][1]"/>
 </xsl:template>
 
 <xsl:template match="paragraph/node()" mode="copy">
  <xsl:copy-of select="."/>
  <xsl:if test="not(following-sibling::node()[1][&dbselfblocks;])">
   <xsl:apply-templates select="following-sibling::node()[1]" mode="copy"/>
  </xsl:if>
 </xsl:template>
</xsl:stylesheet>
