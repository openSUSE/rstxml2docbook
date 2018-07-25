<?xml version="1.0" encoding="utf-8"?>
<!--

-->
<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exsl="http://exslt.org/common"
 extension-element-prefixes="exsl"
 exclude-result-prefixes="exsl">

<xsl:import href="chunker.xsl"/>

<xsl:output method="xml"/>
<xsl:param name="xml.ext">.xml</xsl:param>
<xsl:param name="rootbasename">book</xsl:param>

<xsl:template match="node()|@*">
    <xsl:copy><xsl:apply-templates select="node()|@*"/></xsl:copy>
</xsl:template>

<xsl:template name="get_dirname">
    <xsl:param name="path_to_split"/>
    <xsl:param name="sep">-</xsl:param>
    <xsl:choose>
        <xsl:when test="contains($path_to_split, '/')">
            <xsl:value-of select="concat(substring-before($path_to_split, '/'), $sep)"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$path_to_split"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="get_xml_base">
    <xsl:param name="node" select="."/>
    <xsl:param name="path" select="''"/>
    <xsl:variable name="xmlbase" select="$node/@xml:base"/>
    <xsl:variable name="dir">
        <xsl:call-template name="get_dirname">
            <xsl:with-param name="path_to_split" select="$xmlbase"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="temp_path" select="concat($dir,$path)"/>
    <xsl:if test="$node/..">
        <xsl:call-template name="get_xml_base">
            <xsl:with-param name="node" select="$node/.."/>
            <xsl:with-param name="path" select="$temp_path"/>
        </xsl:call-template>
    </xsl:if>
    <xsl:if test="$node/@xml:base">
        <xsl:value-of select="$dir"/>
    </xsl:if>
</xsl:template>

<xsl:template match="/*|*[@xml:base]">
    <xsl:variable name="xml_base_name" select="@xml:base"/>
    <xsl:variable name="xml_base_file">
        <xsl:variable name="tmp">
            <xsl:call-template name="get_xml_base">
            <xsl:with-param name="node" select="."/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="last_char" select="substring($tmp, string-length($tmp), 1)"/>
        <xsl:choose>
            <xsl:when test="$last_char = '-'">
                 <xsl:value-of select="substring($tmp, 1,string-length($tmp)-1)"/> 
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$tmp"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:variable name="filename">
        <xsl:choose>
            <xsl:when test="not (parent::*)">
                <xsl:value-of select="$rootbasename"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$xml_base_file"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <xsl:call-template name='write.chunk'>
        <xsl:with-param name="method">xml</xsl:with-param>
        <xsl:with-param name="filename" select="concat($basedir, $filename, $xml.ext)"/>
        <xsl:with-param name="indent">yes</xsl:with-param>
        <xsl:with-param name="encoding">UTF-8</xsl:with-param>
        <xsl:with-param name="content">
            <xsl:copy-of select="preceding-sibling::processing-instruction() | preceding-sibling::comment()"/>
            <xsl:copy>
                <xsl:apply-templates select="node()|@*"/>
            </xsl:copy>
        </xsl:with-param>
    </xsl:call-template>

    <xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="{$filename}{$xml.ext}"/>
</xsl:template>

</xsl:stylesheet>