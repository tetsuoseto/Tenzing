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

def _set_proj_common_fields(cs: Dict[str, Any]):
    new_cs: Dict[str, Any] = {
        "doc_template_type": "blank",
        "doc_title_pivot.pt_x": 306,
        "doc_title_pivot.pt_y": 250,
        "doc_toc_title_pivot.pt_x": 306,
        "doc_toc_title_pivot.pt_y": 80, # add 15 for bi-di for optimal result
        "doc_header_pivot.pt_x": 95,
        "doc_header_pivot.pt_y": 16,
        "doc_legal_notice": False,
        "doc_title_font.size": 32,
        "doc_title_font.line_pitch": 50,
        "doc_title_font.line_alignment": "center",
        "doc_subtitle_font.size": 16,
        "doc_subtitle_font.line_pitch": 28,
        "doc_subtitle_font.line_alignment": "center",
        "doc_toc_title_font.size": 24.0,
        "doc_toc_title_font.line_pitch": 50.0,
        "doc_toc_title_font.line_alignment": "center",
        "doc_site_name": "owasp.org",
        "doc_site_url": "https://owasp.org/" + \
            "www-project-application-security-verification-standard/",
        "doc_appendix_title_font.size": 24,
        "doc_appendix_title_font.line_pitch": 35,
        "doc_appendix_title_font.line_alignment": "center",
        "doc_appendix_title_font.color": "black",
        "header_font.color": "black",
        "chapter_pivot.pt_x": 306,
        "chapter_pivot.pt_y": 40,
        "chapter_title_bottom_aligned": False,
        "chapter_font.size": 20,
        "chapter_font.line_pitch": 35,
        "chapter_font.line_alignment": "center",
        "chapter_font.color": "black",
        "section_font.size": 16,
        "section_font.line_pitch": 18.2,
        "blockquote_font.size": 10.0,
        "blockquote_font.line_pitch": 14.0,
        "blockquote_font.line_alignment": "justified",
        "unordered_list_marker": "circle",
        "doc_appendix_titles": [],
        "doc_sponsor_page_titles": [],
    }
    for key in new_cs:
        if cs:
            assert key in cs, \
                f"'{key}' is not defined in customizable styles."
    cs.update(new_cs)

def _set_lang_specific_fields(cs: Dict[str, Any], lang:str):
    cs["doc_title"] = [
        "Doc Title 1",
        "Doc Title 2",
    ]
    cs["doc_subtitles"] = [
        "",
        "",
        "",
        "",
        "doc subtitle 1",
        "doc subtitle 2"
    ]
    cs["doc_revision_history"] = [
        "    2024-11-18 Version 2025 Release"
    ]
    cs["doc_header"] = ""
    cs["doc_toc_contents_title"] = "Table of Contents"
    cs["doc_toc_figures_title"] = "Figures"

def _create_template_pdfs(proj_code, data_dir_path, temp_dir_path):
    use_default_templates = True
    return use_default_templates

# register_project does two things:
#   1. create three template PDFs and store them under data directory
#   2. set the PDF styles
#
# proj_code: for example, "IPS"
# lang_codes: tuple of languages, for example ["en-US"]
# data_dir_path: full path to data directory such as "owasp_pdf_data_IPS"
# get_customizable_styles: callback function
def register_project(proj_code: str, lang_codes: Tuple[str, ...],
        data_dir_path: Path, temp_dir_path: str, get_customizable_styles):

    if proj_code != "ZZZ":
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
            "proj_dir": "zzz",
            "styles": customizable_styles,
            "use_default_templates": use_default_templates,
            }
    return None

def translate_markdown(proj_code: str, lang_code: str, markdown_path: Path,
        temp_dir_path: str):
    assert proj_code == "ZZZ"
    return markdown_path

def _test():

    def get_cust_styles(lang):
        return {}

    dont_care:str = ""
    my_proj_path = os.getcwd()
    data_dir_path = Path(os.path.join(my_proj_path, "owasp_pdf_data_ZZZ"))
    proj_def_generator = register_project("ZZZ", ("en-US",),
        data_dir_path, dont_care, get_cust_styles)
    for proj_def in proj_def_generator:
        assert proj_def["proj_code"] == "ZZZ"
        assert proj_def["lang"] == "en-US"
        assert proj_def["proj_dir"] == "zzz"
        assert isinstance(proj_def["styles"], dict)
    print("Test: success!!")

if __name__ == '__main__':
    _test()
