# -*- coding: utf-8 -*-
#!/usr/bin/env python

class NewspaperCodes:
    
    _language_codes = ["he"]
    
    _newspaper_codes = ["HZT", "HZV", "MGD", "DAV"]
    
    _heb_convert = { 'HZT':u"חבצלת",
                      'HZV':u"חפציבה",
                      'MGD':u"המגיד",
                      'DAV':u"הדוור"}
    
    @classmethod
    def _get_language_dict(cls, language_code):
        if language_code is "he":
            return cls._heb_convert
        
                      
    @classmethod
    def get_code(cls, paper_code, language_code = "he"):
        
        # Test that language code existence
        if language_code not in cls._language_codes:
            language_code = "he"
            
        if paper_code not in cls._newspaper_codes:
            return None
        
        return cls._get_language_dict(language_code)[paper_code]