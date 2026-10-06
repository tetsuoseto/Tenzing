#!/usr/local/bin/python
# pylint: disable=invalid-name

"""
BSD 3-Clause License

Copyright (c) 2024-2026, Tetsuo Seto

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
from pathlib import Path
from typing import Any, Dict, Tuple
from pdb import set_trace

# Standard book bibliopegy (in Tenzing5 terms):
#  1. Half-title page
#  2. Title page (cover page)
#  3. Copyright page (legal notice)
#  4. Dedication and/or epigraph
#  5. Table of contents (toc/contents)
#  6. Lists of tables or illustrations (toc/figures&tables)
#    (all others are body contents and page-numbered)
#    "doc_pages_to_front: 4" means that move the first 4 numbered pages
#    between legal notice and TOC.
#    The first 4 pages are not numbered and page numbering starts at the
#    fifth body content page.
#  7. Foreword
#  8. Preface
#  9. Acknowledgments
# 10. Introduction

def _set_proj_common_fields(cs: Dict[str, Any]):
    new_cs: Dict[str, Any] = {
        "doc_template_type": "blank",
        "doc_title_pivot.pt_x": 306,
        "doc_title_pivot.pt_y": 250,
        "doc_toc_title_pivot.pt_x": 306,
        "doc_toc_title_pivot.pt_y": 80, # add 15 for bi-di for optimal result
        "doc_header_pivot.pt_x": 95,
        "doc_header_pivot.pt_y": 16,
        "doc_cover": False,
        "doc_pages_to_front": 5,
        "doc_title": [],
        "doc_title_font.size": 30,
        "doc_title_font.line_pitch": 45,
        "doc_title_font.line_alignment": "center",
        "doc_subtitles": [],
        "doc_header": "",
        "doc_subtitle_font.size": 16,
        "doc_subtitle_font.line_pitch": 28,
        "doc_subtitle_font.line_alignment": "center",
        "doc_toc_title_font.size": 24.0,
        "doc_toc": True,
        "doc_toc_contents_title": "",
        "doc_toc_figures_title": "",
        "doc_toc_translations": [],
        "doc_toc_title_font.line_pitch": 50.0,
        "doc_toc_title_font.line_alignment": "center",
        "doc_site_name": "",
        "doc_site_url": "",
        "doc_legal_notice": False,
        "doc_watermark": False,
        "doc_appendix_titles": [],
        "doc_sponsor_page_titles": [],
        "doc_appendix_title_font.size": 13.0,
        "doc_appendix_title_font.line_pitch": 18.2,
        "doc_appendix_title_font.line_alignment": "left",
        "doc_appendix_title_font.color": "black",
        "header_font.color": "black",
        "chapter_pivot.pt_x": 306,
        "chapter_pivot.pt_y": 72,
        "chapter_title_bottom_aligned": False,
        "chapter_font.size": 20,
        "chapter_font.line_pitch": 35,
        "chapter_font.line_alignment": "center",
        "chapter_font.color": "black",
        "section_font.size": 16,
        "section_font.line_pitch": 18.2,
        "blockquote_font.size": 10.0,
        "blockquote_font.line_pitch": 13.0,
        "blockquote_font.line_alignment": "justified",
        "blockquote_stylesheet": [
            ["bss-pagecolor", "PC", "darkslategray|white"],
            ["bss-pagecolor.spacewide", "PCWIDE", "||||260"],
            ["bss-pagecolor.spacenarrow", "PCNARR", "||||50"],
            ["bss-pagecolor.center", "PCC", "||center"],
            ["bss-pagecolor.center.large", "PCCL", "|||80|90|hb"],
            ["bss-pagecolor.center.small", "PCCS", "|||20|28|hr"],
            ["bss-center", "C", "||center|||br"],
            ["bss-center.medium", "CM", "|||20|28"],
            ["bss-center.small", "CS", "|||15|20"],
            ["bss-center.verysmall", "CVS", "|||10|14"]
        ],
        "reference_font.size": 10.0,
        "reference_font.line_pitch": 14.0,
        "reference_font.line_alignment": "left",
        "unordered_list_marker": "circle",
        "md_file_translation_data_sheet": 500,
        "md_file_range": [100, 500],
        "max_image_scale": 2.0
    }
    for key in new_cs:
        if cs:
            assert key in cs, \
                f"'{key}' is not defined in customizable styles."
    cs.update(new_cs)

def _set_lang_specific_fields(cs: Dict[str, Any], lang:str):
    if lang in ("ar-SA", "he-IL", "fa-IR"):
        cs["doc_toc_title_font.line_alignment"] = "right"
        cs["chapter_font.line_alignment"] = "right"
        cs["section_font.line_alignment"] = "right"
        cs["reference_font.line_alignment"] = "right"
        cs["doc_toc_font.line_alignment"] = "right"
    else:
        cs["doc_toc_title_font.line_alignment"] = "left"
        cs["chapter_font.line_alignment"] = "left"
        cs["section_font.line_alignment"] = "left"
        cs["reference_font.line_alignment"] = "left"
        cs["doc_toc_font.line_alignment"] = "left"
    # Letter paper size
    if lang in ("en-US", "fr-CA", "es-MX"):
        cs["blockquote_stylesheet"] = [
            ["bss-pagecolor", "PC", "darkslategray|white"],
            ["bss-pagecolor.spacewide", "PCWIDE", "||||220"],
            ["bss-pagecolor.spacenarrow", "PCNARR", "||||50"],
            ["bss-pagecolor.center", "PCC", "||center"],
            ["bss-pagecolor.center.large", "PCCL", "|||70|80|hb"],
            ["bss-pagecolor.center.small", "PCCS", "|||18|25|hr"],
            ["bss-center", "C", "||center|||br"],
            ["bss-center.medium", "CM", "|||18|25"],
            ["bss-center.small", "CS", "|||15|20"],
            ["bss-center.verysmall", "CVS", "|||10|14"]
        ]
    if lang in ("km-KH", "lo-LA", "my-MM"):
        cs["body_font.line_alignment"] = "left"
        cs["blockquote_font.line_alignment"] = "left"
        # taller line_pitch makes font matter longer
        cs["doc_pages_to_front"] += 1
        # make line_pitch double of font_size
        # height goes way up for ligature
        cs["doc_title_font.line_pitch"] = \
            cs["doc_title_font.size"]*2
        cs["doc_subtitle_font.line_pitch"] = \
            cs["doc_subtitle_font.size"]*2
        cs["doc_toc_title_font.line_pitch"] = \
            cs["doc_toc_title_font.size"]*2
        cs["doc_toc_font.line_pitch"] = \
            cs["doc_toc_font.size"]*2
        cs["doc_appendix_title_font.line_pitch"] = \
            cs["doc_appendix_title_font.size"]*2
        cs["chapter_font.line_pitch"] = \
            cs["chapter_font.size"]*2
        cs["section_font.line_pitch"] = \
            cs["section_font.size"]*2
        cs["block_font.line_pitch"] = \
            cs["block_font.size"]*2
        cs["block6_font.line_pitch"] = \
            cs["block6_font.size"]*2
        cs["caption_font.line_pitch"] = \
            cs["caption_font.size"]*2
        cs["body_font.line_pitch"] = \
            cs["body_font.size"]*2
        cs["reference_font.line_pitch"] = \
            cs["reference_font.size"]*2
        cs["blockquote_font.line_pitch"] = \
            cs["blockquote_font.size"]*2
        cs["blockquote_stylesheet"] = [
            ["bss-pagecolor", "PC", "darkslategray|white"],
            ["bss-pagecolor.spacewide", "PCWIDE", "||||200"],
            ["bss-pagecolor.spacenarrow", "PCNARR", "||||50"],
            ["bss-pagecolor.center", "PCC", "||center"],
            ["bss-pagecolor.center.large", "PCCL", "|||80|160|hb"],
            ["bss-pagecolor.center.small", "PCCS", "|||20|40|hr"],
            ["bss-center", "C", "||center|||br"],
            ["bss-center.medium", "CM", "|||20|40"],
            ["bss-center.small", "CS", "|||15|30"],
            ["bss-center.verysmall", "CVS", "|||10|20"]
        ]

def _create_template_pdfs(proj_code, data_dir_path, temp_dir_path):
    use_default_templates = True
    return use_default_templates

# register_project does two things:
#   1. create three template PDFs and store them under data directory
#   2. set the PDF styles
def register_project(proj_code: str, lang_codes: Tuple[str, ...],
        data_dir_path: Path, temp_dir_path: str, get_customizable_styles):

    if proj_code != "COE":
        return None

    use_default_templates = _create_template_pdfs(
        proj_code, data_dir_path, temp_dir_path)
    for lang in lang_codes:
        customizable_styles: Dict[str, Any] = get_customizable_styles(lang)
        _set_proj_common_fields(customizable_styles)
        _set_lang_specific_fields(customizable_styles, lang)
        yield {
            "proj_code": proj_code,
            "lang": lang,
            "proj_dir": "coe",
            "styles": customizable_styles,
            "use_default_templates": use_default_templates,
            }
    return None

def translate_markdown(proj_code: str, lang_code: str, markdown_path: Path,
        temp_dir_path: str, doc_toc_translations: list):
    assert proj_code == "COE"
    return markdown_path

def _test():

    def get_cust_styles(lang):
        return {}

    dont_care:str = ""
    my_proj_path = os.getcwd()
    data_dir_path = Path(os.path.join(my_proj_path, "tenzing_data_COE"))
    proj_def_generator = register_project("COE", ("en-US",),
        data_dir_path, dont_care, get_cust_styles)
    for proj_def in proj_def_generator:
        assert proj_def["proj_code"] == "COE"
        assert proj_def["lang"] == "en-US"
        assert proj_def["proj_dir"] == "coe"
        assert isinstance(proj_def["styles"], dict)
    print("Test: success!!")

if __name__ == '__main__':
    _test()
