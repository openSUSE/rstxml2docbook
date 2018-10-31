<?xml version="1.0" encoding="UTF-8"?>
<!--
   Purpose:
     Moves block elements inside <paragraphs> outside of <paragraphs>.

   Parameters:
     None

   Input:
     RST XML file.

   Output:
     RST XML file, but without block element inside <paragraph>s.

   Example:
     See https://github.com/openSUSE/rstxml2docbook/issues/76

   Author:
     Thomas Schraitle <toms AT opensuse.org>
     Copyright 2018 SUSE Linux GmbH

-->
<!DOCTYPE xsl:stylesheet
[
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
  <xsl:template match="entry/inline | entry/emphasis | entry/strong |
                       list_item/strong | list_item/literal | list_item/emphasis">
  <paragraph>
   <xsl:copy>
    <xsl:copy-of select="@*"/>
    <xsl:apply-templates/>
   </xsl:copy>
  </paragraph>
 </xsl:template>

</xsl:stylesheet>
