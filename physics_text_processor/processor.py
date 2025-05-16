import re
import unicodedata
from typing import Dict, List, Union, Optional
import ftfy
from collections import defaultdict

class RobustPhysicsTextProcessor:
    def __init__(self, 
                 preserve_unicode: bool = True,
                 aggressive_clean: bool = False,
                 language_support: str = 'multilingual'):
        """
        Full-featured physics text processor
        
        Args:
            preserve_unicode: Keep scientific symbols (μ, α, etc.)
            aggressive_clean: Remove all non-ASCII when False
            language_support: 'latin', 'multilingual', or 'full'
        """
        self.preserve_unicode = preserve_unicode
        self.aggressive_clean = aggressive_clean
        self.language_support = language_support
        self.processing_stats = defaultdict(int)

        # Physics symbol mappings (unicode ↔ text)
        self.symbol_map = {
            'alpha': 'α', 'beta': 'β', 'gamma': 'γ',
            'mu': 'μ', 'theta': 'θ', 'lambda': 'λ',
            'delta': 'δ', 'sigma': 'σ', 'omega': 'ω',
            'Delta': 'Δ', 'nabla': '∇', 'partial': '∂'
        }

    def _handle_unicode(self, text: str) -> str:
        """Convert between unicode symbols and text representations"""
        if self.preserve_unicode:
            # Convert text to unicode (alpha → α)
            for word, symbol in self.symbol_map.items():
                text = re.sub(rf'\b{word}\b', symbol, text)
        else:
            # Convert unicode to text (α → alpha)
            for word, symbol in self.symbol_map.items():
                text = text.replace(symbol, word)
        return text

    def _clean_scientific_notation(self, text: str) -> str:
        """Standardize 1.23×10⁻⁵ formats"""
        # Handle both "1.23x10^-5" and "1.23e-5"
        text = re.sub(
            r'([0-9.]+)\s*[x×]\s*10\s*[\^\(\)]*([+-]?[0-9]+)',
            lambda m: f"{m.group(1)}×10<sup>{m.group(2)}</sup>" 
                     if self.preserve_unicode 
                     else f"{m.group(1)}x10^{m.group(2)}",
            text
        )
        text = re.sub(
            r'([0-9.]+)\s*[eE]\s*([+-]?[0-9]+)',
            lambda m: f"{m.group(1)}×10<sup>{m.group(2)}</sup>"
                     if self.preserve_unicode
                     else f"{m.group(1)}e{m.group(2)}",
            text
        )
        return text

    def _detect_sections(self, text: str) -> Dict[str, str]:
        """Identify physics document sections"""
        sections = {}
        # Constants table detection
        const_match = re.search(
            r'(?:fundamental\s+)?constants?[\s\S]+?(?=\n\s*\n)', 
            text, re.IGNORECASE
        )
        if const_match:
            sections['constants'] = const_match.group(0)
        
        # Equations detection
        eq_match = re.search(
            r'(?:key\s+)?equations?[\s\S]+?(?=\n\s*\n)',
            text, re.IGNORECASE
        )
        if eq_match:
            sections['equations'] = eq_match.group(0)
            
        return sections

    def process(self, text: Optional[str]) -> Dict[str, Union[str, Dict]]:
        """Full processing pipeline"""
        if not text:
            return {"error": "Empty input"}

        try:
            # Encoding fixes
            text = ftfy.fix_text(text)
            
            # Unicode normalization
            text = unicodedata.normalize('NFKC', text)
            
            # Core cleaning
            text = self._handle_unicode(text)
            text = self._clean_scientific_notation(text)
            
            # Section analysis
            sections = self._detect_sections(text)
            
            return {
                "cleaned_text": text,
                "sections": sections,
                "stats": dict(self.processing_stats)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "original_text": text[:500] + ('...' if len(text) > 500 else '')
            }