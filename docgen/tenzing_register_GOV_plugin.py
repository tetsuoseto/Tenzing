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
import shutil
from typing import Any, Dict, Tuple

from PIL import Image
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen.canvas import Canvas # type: ignore
from reportlab.lib.pagesizes import A4, LETTER # type: ignore

LETTER_PAPER_LANGS = ["en-US", "es-MX", "fr-CA"]

def _set_proj_common_fields(cs: Dict[str, Any]):
    new_cs: Dict[str, Any] = {
        "doc_template_type": "custom",
        "doc_title_pivot.pt_x": 300,
        "doc_title_pivot.pt_y": 350,
        "doc_toc": True,
        "doc_authors_toc": False,
        "doc_toc_title_pivot.pt_x": 72,
        "doc_toc_title_pivot.pt_y": 72,
        "doc_header": "",
        "doc_header_pivot.pt_x": 72,
        "doc_header_pivot.pt_y": 36,
        "doc_legal_notice": False,
        "doc_title_font.size": 40,
        "doc_title_font.line_pitch": 48,
        "doc_title_font.line_alignment": "center",
        "doc_title_font.color": "white",
        "doc_subtitle_font.size": 16,
        "doc_subtitle_font.line_pitch": 24,
        "doc_subtitle_font.line_alignment": "center",
        "doc_subtitle_font.color": "lightskyblue",
        "doc_toc_title_font.size": 24.0,
        "doc_toc_title_font.line_pitch": 50.0,
        "doc_toc_title_font.line_alignment": "left",
        "doc_site_name": "",
        "doc_site_url": "",
        "doc_appendix_title_font.size": 13.0,
        "doc_appendix_title_font.line_pitch": 18.2,
        "doc_appendix_title_font.line_alignment": "left",
        "doc_appendix_title_font.color": "black",
        "chapter_pivot.pt_x": 72,
        "chapter_pivot.pt_y": 72,
        "chapter_title_bottom_aligned": False,
        "chapter_font.size": 0.1,
        "chapter_font.line_pitch": 0.1,
        "chapter_font.line_alignment": "left",
        "chapter_font.color": "white",
        "section_font.size": 0.1,
        "section_font.line_pitch": 0.1,
        "section_font.line_alignment": "left",
        "section_font.color": "white",
        "block_font.size": 12,
        "block_font.line_pitch": 14,
        "block_font.color": "black",
        "block6_font.size": 9,
        "block6_font.line_pitch": 11,
        "block6_font.color": "black",
        "header_font.color": "black",
        "footer_font.color": "black",
        "body_font.size": 10.0,
        "body_font.line_pitch": 13.0,
        "blockquote_font.size": 10.0,
        "blockquote_font.line_pitch": 13.0,
        "blockquote_font.line_alignment": "justified",
        "reference_font.size": 8.0,
        "reference_font.line_pitch": 10.0,
        "reference_font.line_alignment": "left",
        "unordered_list_marker": "circle",
        "max_image_scale": 1.3,
    }
    for key in new_cs:
        if cs:
            assert key in cs, \
                f"'{key}' is not defined in customizable styles."
    cs.update(new_cs)

def _set_lang_specific_fields(cs: Dict[str, Any], lang:str):
    cs["doc_title"] = [
        "INTERNATIONAL",
        "AI SAFETY REPORT",
        "2026",
    ]
    cs["doc_subtitles"] = [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "February 2026"
    ]
    cs["doc_revision_history"] = [
        "    2026-02-03 February 2026 Release",
    ]
    cs["doc_toc_contents_title"] = "Contents"
    cs["doc_toc_figures_title"] = "Figures and Tables"
    cs["doc_toc_translations"] = [
        "Table:Table", "Figure:Figure", "Box:Box"]
    cs["doc_appendix_titles"] = []
    cs["doc_sponsor_page_titles"] = []
    if lang in ("ar-SA", "he-IL", "fa-IR"):
        cs["doc_toc_title_font.line_alignment"] = "right"
        cs["chapter_font.line_alignment"] = "right"
        cs["section_font.line_alignment"] = "right"
        cs["reference_font.line_alignment"] = "right"
    else:
        cs["doc_toc_title_font.line_alignment"] = "left"
        cs["chapter_font.line_alignment"] = "left"
        cs["section_font.line_alignment"] = "left"
        cs["reference_font.line_alignment"] = "left"
    if cs["doc_title_font.line_alignment"] == "center":
        cs["doc_title_pivot.pt_x"] = 306 if lang in LETTER_PAPER_LANGS else 298

def _merge_pdf(output_pdf, base_pdf, overlay_pdf):
    overlay = PdfReader(overlay_pdf).pages[0]
    base_page = PdfReader(base_pdf).pages[0]
    writer = PdfWriter()
    base_page.merge_page(overlay)
    writer.add_page(base_page)
    with open(output_pdf, "wb") as out_file:
        writer.write(out_file)
    writer.close()
    return output_pdf

def _create_cover_page(paper_size: Tuple, paper_size_str: str,
        data_dir_path: Path, temp_dir_path: str, proj_code: str):
    page_name: str = f"1_{proj_code}_cover_{paper_size_str}.pdf"
    page_path = os.path.join(data_dir_path,
        "templates/page_pdfs", page_name)
    image_file_path = os.path.join(data_dir_path,
        "templates/image_parts/cover_background.png") # monotone.png
    bkgd_img = Image.open(image_file_path)
    img_width, img_height = bkgd_img.size
    img_aspect = img_height / float(img_width)
    print_width = paper_size[0]
    print_height = print_width * img_aspect

    canvas = Canvas(page_path, pagesize=paper_size)
    canvas.drawImage(image_file_path, \
        0.0, paper_size[1] - print_height, \
        print_width, print_height
        )
    canvas.showPage()
    canvas.save()

def _create_blank_page(paper_size: Tuple, paper_size_str: str,
        data_dir_path: Path, temp_dir_path: str, temp_type: str,
        proj_code: str):
    assert temp_type in ["toc", "body", "chapter"]
    temp_id: int = 4 if temp_type == "toc" else 3 if \
        temp_type == "body" else 2
    page_name = f"{temp_id}_{proj_code}_{temp_type}_{paper_size_str}.pdf"
    page_path = data_dir_path/"templates/page_pdfs"/page_name
    canvas = Canvas(str(page_path), pagesize=paper_size)
    canvas.showPage()
    canvas.save()

def _copy_template_pdfs_RtoL(data_dir_path, proj_code):
    paper_sizes = ["LETTER", "A4"]
    pdf_path = data_dir_path/"templates/page_pdfs"
    place_holder = "{}"
    templates = [
        f"1_{proj_code}_cover_{place_holder}{place_holder}.pdf",
        f"2_{proj_code}_chapter_{place_holder}{place_holder}.pdf",
        f"3_{proj_code}_body_{place_holder}{place_holder}.pdf",
        f"4_{proj_code}_toc_{place_holder}{place_holder}.pdf",
        ]
    for paper_size in paper_sizes:
        for template in templates:
            src = pdf_path/template.format(paper_size, "")
            dst = pdf_path/template.format(paper_size, "_RtoL")
            shutil.copyfile(src, dst)

def _create_template_pdfs(proj_code, data_dir_path, temp_dir_path):
    paper_sizes = [LETTER, A4]
    for paper_size in paper_sizes:
        paper_size_str = "LETTER" if paper_size == LETTER else "A4"
        _create_cover_page(paper_size, paper_size_str,
            data_dir_path, temp_dir_path, proj_code)
        _create_blank_page(paper_size, paper_size_str,
            data_dir_path, temp_dir_path, "body", proj_code)
        _create_blank_page(paper_size, paper_size_str,
            data_dir_path, temp_dir_path, "toc", proj_code)
        _create_blank_page(paper_size, paper_size_str,
            data_dir_path, temp_dir_path, "chapter", proj_code)
    _copy_template_pdfs_RtoL(data_dir_path, proj_code)
    use_default_templates = False
    return use_default_templates

# register_project does two things:
#   1. create three template PDFs and store them under data directory
#   2. set the PDF styles
#
# proj_code: for example, "OLM"
# lang_codes: tuple of languages, for example ["en-US"]
# data_dir_path: full path to data directory "tenzing_data_OLM"
# get_customizable_styles: callback function
# temp_dir_path: temporary directory path
def register_project(proj_code: str, lang_codes: Tuple[str, ...],
        data_dir_path:Path, temp_dir_path: str, get_customizable_styles):

    if proj_code != "GOV":
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
            "proj_dir": "gov",
            "styles": customizable_styles,
            "use_default_templates": use_default_templates,
            }
    return None

def translate_markdown(proj_code: str, lang_code: str, markdown_path: Path,
        temp_dir_path: str, doc_toc_translations: list):
    assert proj_code == "GOV"
    return markdown_path

def _test():

    def get_cust_styles(lang):
        return {}

    dont_care:str = ""
    my_proj_path = os.getcwd()
    data_dir_path = Path(os.path.join(my_proj_path, "tenzing_data_GOV"))
    proj_def_generator = register_project("GOV", ("en-US",),
        data_dir_path, dont_care, get_cust_styles)
    for proj_def in proj_def_generator:
        assert proj_def["proj_code"] == "GOV"
        assert proj_def["lang"] == "en-US"
        assert proj_def["proj_dir"] == "gov"
        assert isinstance(proj_def["styles"], dict)
    print("Test: success!!")

if __name__ == '__main__':
    _test()
