# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 21:20:28 2016

@author: gxy
"""
from pyPdf import PdfFileWriter,PdfFileReader
import cookielib
import urllib2
import urllib
import string
import sys
from BeautifulSoup import BeautifulSoup

class ThesisInfo(object):
    def __init__(self):
        self.title =''
        self.authors = []
        self.abstract = ''
        self.publish = ''
        self.year = ''
        self.volume = ''
        self.number = ''
        self.pages = ''
        self.keywords = []
    
    def setInfo(self,info):
        [self.title,self.authors,self.abstract,self.publish,self.year,self.volume,self.number,self.pages,self.keywords]=info

class Thesis(object):
    def __init__(self,stream):
        #self.stream = stream
        self.title = self.getTitle(stream)
        self.info = ThesisInfo()
        
    def getInfo(self):
        self.info = self._getInfoFromWeb(self.title,'baidu')
    
    def printInfo(self):
        infoList = [ '【title】:   '+self.info.title]
        infoList.append( '【authors】: '+','.join(self.info.authors))
        infoList.append( '【abstract】:'+self.info.abstract)
        infoList.append( '【publish】: '+self.info.publish)
        infoList.append( '【year】:    '+self.info.year)
        infoList.append( '【volume】:  '+self.info.volume)
        infoList.append( '【number】:  '+self.info.number)
        infoList.append( '【pages】:   '+self.info.pages)
        infoList.append( '【keywords】:'+','.join(self.info.keywords))
        infoStr = '\n'.join(infoList)
        print infoStr
        return infoStr
    
    def _getInfoFromWeb(self,title,web):
        thesisInfo = ThesisInfo()
        try:
            if web == 'baidu':
                baseUrl = 'http://xueshu.baidu.com'
                cj = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
                urllib2.install_opener(opener)
                #title = 'Analysis of HTEM Horn-Type Antenna for High-Power Impulse Radiation Applications'
                word = 'intitle:(%s)'%title
                para = urllib.urlencode({'wd':word,'tn':'SE_baiduxueshu_c1gjeupa','bs':'','ie':'utf-8','sc_f_para':'sc_tasktype={firstAdvancedSearch}'})
                data = opener.open(baseUrl+'/s?'+para).read()
                h3s = BeautifulSoup(data)('h3')
                results = [h3 for h3 in h3s if h3.get('class')=='t c_font']
                # The list is sorted by relativity from high to low, 
                #select the most relative title,that is, the first one
                href = (results[0]('a'))[0].get('href')
                dataPage = opener.open(baseUrl+href).read()
                divs = BeautifulSoup(dataPage)('div')
                for div in divs:
                    if div.get('data-click')=="{'act_block':'main'}":
                        break
                webTitle = ((div('h3')[0])('a')[0]).text
                for p in div('p'):
                    if p.get('class')=='author_text':
                        webAuthors = [a.text for a in p('a')]
                    if p.get('class')=='abstract':
                        webAbstract = p.text
                    if p.get('class')=='publish_text':
                        webPublish = (p('a')[0]).text
                        publishDetail =[span.text for span in p('span')]
                        if len(publishDetail)==4:
                            [webYear,webVolume,webNumber,webPages]=publishDetail
                    if p.get('class')=='kw_main':
                        webKeywords = [a.text for a in p('a')]
            thesisInfo.setInfo([webTitle,webAuthors,webAbstract,webPublish,webYear,webVolume,webNumber,webPages,webKeywords])
        except Exception,e:
            print e
        return thesisInfo
                    
            
    def getTitle(self,stream):
        stream.seek(0)
        input1 = PdfFileReader(stream)
        title = input1.getDocumentInfo().title
        # if fail to get thesis's title , we deal with it by using a special algorithm.
        if title in ['untitled','']:
            from pdfminer.pdfdocument import PDFDocument
            from pdfminer.pdfparser import PDFParser
            from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
            from pdfminer.pdfdevice import PDFDevice, TagExtractor
            from pdfminer.pdfpage import PDFPage
            from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
            from pdfminer.layout import LAParams
            try:
                from cStringIO import StringIO
            except ImportError:
                from StringIO import StringIO
            # init parameters
            caching = True
            codec = 'utf-8'
            imagewriter = None
            stripcontrol = False
            pagenos = set()
            password = ''
            maxpages = 0
            rotation = 0
            rsrcmgr = PDFResourceManager(caching=caching)
            laparams = LAParams()
            outfp = StringIO()
            # convert pdf to xml, using StringIO to store XML
            device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                              imagewriter=imagewriter,
                              stripcontrol=stripcontrol)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            pagenos.update( int(x)-1 for x in '1'.split(',') )
            stream.seek(0)
            for page in PDFPage.get_pages(stream, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
                page.rotate = (page.rotate+rotation) % 360
                interpreter.process_page(page)
            device.close()
            outfp.seek(0)
            # parse the xml to get title
            title = self._getTitleFromXmlStr(outfp.read().encode(codec))
        return title
    
    def _getTitleFromXmlStr(self,xmlStr):

        '''
        By observing many theses, we find some characteristics of title:
            1. title use large font, sometime not the largest, e.g. the first 
            letter of the first word in Introduction is the largest in some 
            IEEE thesis, sometimes the largest word is Author.
            2. the word in title use the same font, which is different from the
            first word in Introduction.
            3. title always appear in the first page of the thesis
        '''
        from lxml import etree
        try:
            root = etree.fromstring(xmlStr) #return element, the root
            page = root.find('page')
            texts = page.findall('textbox/textline/text')
            textsFont = []
            textsWord =[]
            for endText in texts:
                fontStr = endText.get('size')
                if fontStr:
                    textsFont.append(float(fontStr))
                else:
                    textsFont.append(0)
                textsWord.append(endText.text)
            fontsList = list(set(textsFont))
            fontsList.sort(reverse=True)
            #print fontsList
            titleCandidate = []
            # select the three largest font words
            for font in fontsList[:3]:
                tempStr = ''.join([textsWord[i] for i in xrange(len(textsFont)) if textsFont[i] in (font,0) ]).strip()
                titleCandidate.append(' '.join(tempStr.split()))
            title = titleCandidate[0] if len(titleCandidate[0])>10 else (titleCandidate[1] if len(titleCandidate[1])>10 else titleCandidate[2])
        #    for tit in titleCandidate:
            return title
        except Exception,e:
            print e
            return ''

if __name__ == "__main__":
    fileName = '06814290.pdf'
    fileHandle = file(fileName,'rb')
    Thesis(fileHandle).printInfo()
    fileHandle.close()