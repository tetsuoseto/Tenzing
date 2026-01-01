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
import os.path
from pathlib import Path
import re
import shutil
from typing import Any, Dict, List, Tuple
from pdb import set_trace # pylint: disable=unused-import

def _set_proj_common_fields(cs: Dict[str, Any]):
    new_cs: Dict[str, Any] = {
        "doc_template_type": "modern_blue",
        "doc_title_pivot.pt_x": 72,
        "doc_title_pivot.pt_y": 440,
        "doc_toc_title_pivot.pt_x": 72,
        "doc_toc_title_pivot.pt_y": 172, # add 15 for bi-di for optimal result
        "doc_header": " ",
        "doc_header_pivot.pt_x": 100,
        "doc_header_pivot.pt_y": 16,
        "doc_legal_notice": False,
        "doc_title_font.size": 33,
        "doc_title_font.line_pitch": 40,
        "doc_title_font.line_alignment": "left",
        "doc_subtitle_font.size": 16,
        "doc_subtitle_font.line_pitch": 24,
        "doc_subtitle_font.line_alignment": "left",
        "doc_toc_title_font.size": 24.0,
        "doc_toc_title_font.line_pitch": 50.0,
        "doc_toc_title_font.line_alignment": "left",
        "doc_site_name": "owasp.org",
        "doc_site_url": "https://owasp.org/" + \
            "www-project-application-security-verification-standard/",
        "doc_appendix_title_font.size": 13.0,
        "doc_appendix_title_font.line_pitch": 18.2,
        "doc_appendix_title_font.line_alignment": "left",
        "doc_appendix_title_font.color": "black",
        "header_font.color": "white",
        "chapter_pivot.pt_x": 72,
        "chapter_pivot.pt_y": 130,
        "chapter_title_bottom_aligned": False,
        "chapter_font.size": 20,
        "chapter_font.line_pitch": 35,
        "chapter_font.line_alignment": "left",
        "chapter_font.color": "black",
        "section_font.size": 16,
        "section_font.line_pitch": 18.2,
        "blockquote_font.size": 10.0,
        "blockquote_font.line_pitch": 14.0,
        "blockquote_font.line_alignment": "justified",
        "reference_font.line_alignment": "left",
        "unordered_list_marker": "circle",
    }
    for key in new_cs:
        if cs:
            assert key in cs, \
                f"'{key}' is not defined in customizable styles."
    cs.update(new_cs)

def _set_lang_specific_fields(cs: Dict[str, Any], lang:str):
    cs["doc_title"] = [
        "Artificial Intelligence",
        "Security Verification",
        "Standard",
    ]
    cs["doc_subtitles"] = [
        "",
        "",
        "",
        "",
        "Initial Version Work In Progress",
        "",
        "",
        "_______ ___, 2026"
    ]
    cs["doc_revision_history"] = [
        "    2026-__-__  1.0  English Version Release",
    ]
    cs["doc_toc_contents_title"] = "Table of Contents"
    cs["doc_toc_figures_title"] = "Figures"
    cs["doc_appendix_titles"] = []
    cs["doc_sponsor_page_titles"] = [
        "Project Sponsors", "Supporting Organizations"]
    if lang in ("ar-SA", "he-IL", "fa-IR"):
        cs["doc_title_font.line_alignment"] = "right"
        cs["doc_subtitle_font.line_alignment"] = "right"
        cs["doc_toc_title_font.line_alignment"] = "right"
        cs["chapter_font.line_alignment"] = "right"
        cs["reference_font.line_alignment"] = "right"
    else:
        cs["doc_title_font.line_alignment"] = "left"
        cs["doc_subtitle_font.line_alignment"] = "left"
        cs["doc_toc_title_font.line_alignment"] = "left"
        cs["chapter_font.line_alignment"] = "left"
        cs["reference_font.line_alignment"] = "left"

def _create_template_pdfs(proj_code, data_dir_path, temp_dir_path):
    use_default_templates = True
    return use_default_templates

# register_project does two things:
#   1. create three template PDFs and store them under data directory
#   2. set the PDF styles
#
# proj_code: for example, "OLM"
# lang_codes: tuple of languages, for example ["en-US"]
# data_dir_path: full path to data directory "owasp_pdf_data_OLM"
# get_customizable_styles: callback function
# temp_dir_path: temporary directory path
def register_project(proj_code: str, lang_codes: Tuple[str, ...],
        data_dir_path:Path, temp_dir_path: str, get_customizable_styles):

    if proj_code != "ASV":
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
            "proj_dir": "asv",
            "styles": customizable_styles,
            "use_default_templates": use_default_templates,
            }
    return None

DFLT_LEVEL_COLORS = ["ghostwhite", "ghostwhite"]
LEVEL_COLORS = {
    1: ["mistyrose", "mistyrose"], # [head line color, description color]
    2: ["yellow", "yellow"],
    3: ["palegreen", "palegreen"],
}

def translate_markdown(proj_code: str, lang_code: str, markdown_path: Path,
        temp_dir_path: str):
    # pylint: disable=too-many-statements, too-many-branches, too-many-locals
    assert proj_code == "ASV"

    def compile_two_lines(headers: List[str], contents: List[str],
            raw_line: str = ""):
        assert len(headers) == len(contents), \
            f"Check MD line: {raw_line}"
        level: int = 0
        level_str: str = "TRANS ERR"
        try:
            level = int(contents[2])
            level_str = str(level)
            level_colors = LEVEL_COLORS.get(level, DFLT_LEVEL_COLORS)
        except Exception:
            level_colors = DFLT_LEVEL_COLORS
        line1: str = ">"+level_colors[0]+"|black||||hb  "+\
            headers[0]+contents[0]
        if len(headers) == 4:
            line1 += ("    "+headers[2]+": "+level_str)
        line1 += ("    "+headers[-1]+": "+str(contents[-1]))
        line2: str = ">"+level_colors[1]+"|black  "+contents[1]
        return line1, line2

    re_sharp = "^([\\#]+)( .*)$"
    re_exclam = "^(\\!\\[)(.*)$"
    re_bar = "^[\\|｜][^\\|｜].*$"
    re_id_num = f"^{proj_code}([0-9]+)_"
    re_special_color = r"^[#]{4}.+([1-3一二三])"

    basename = os.path.basename(markdown_path)
    assert basename.endswith(".md")
    matched = re.match(re_id_num, basename)
    id_num = int(matched.group(1) if matched else -1)
    convered_path = os.path.join(temp_dir_path, "converted.md")
    with open(convered_path, "w", encoding="UTF-8") as out_fp:
        with open(markdown_path, "r", encoding="UTF-8") as md_fp:
            is_processing_table: bool = False
            headers: List[str] = []
            # pylint: disable=too-many-nested-blocks
            for raw_line in md_fp.readlines():
                raw_line_orig = raw_line
                if raw_line[-1] != "\n":
                    raw_line += "\n"
                assert raw_line[-1] == "\n", \
                    f"Check MD line: {raw_line}"
                raw_line = raw_line[:-1].strip()
                skip_write: bool = False
                if raw_line == "\n":
                    out_fp.write(raw_line)
                    continue
                # special color addition
                #-----------------------
                if id_num == 1003:
                    matched = re.match(re_special_color, raw_line)
                    if matched:
                        # raw_line : "#### Level 1 requirements"
                        # raw_line : "#### 一级要求"
                        num_str = matched.group(1)
                        try:
                            level_num = int(num_str)
                        except Exception:
                            if num_str == "一":
                                level_num = 1
                            elif num_str == "二":
                                level_num = 2
                            else:
                                level_num = 3
                        out_str = f">{LEVEL_COLORS[level_num][0]}" + \
                            "|black||||hb  " + raw_line[5:] + "\n"
                        out_fp.write(out_str)
                        continue
                # sharp tag adjustment
                #-----------------------
                # "---"?
                if raw_line == "---":
                    out_fp.write(">white|black|center|||mr " + "─"*40 + "\n")
                    continue
                #-----------------------
                # Does the line start with "#"?
                matched = re.match(re_sharp, raw_line)
                if matched:
                    raw_line = matched.group(1) + "#" + matched.group(2) + "\n"
                    out_fp.write(raw_line)
                    continue
                # image directory adjustment
                #-----------------------
                # from "../images/license.png" to "images/license.png"
                # Does the line start with "!"?
                matched = re.match(re_exclam, raw_line)
                if matched:
                    raw_line = raw_line.replace("../images", "images")
                    out_fp.write(raw_line)
                    continue

                # table translation
                #-----------------------
                # Does the line start with "|" or "｜"?
                matched = re.match(re_bar, raw_line)
                if matched and matched.group(0):
                    # table detected
                    if id_num == 1001:
                        if is_processing_table:
                            assert len(headers) > 0, \
                                f"Check MD line: {raw_line}"
                            contents = [content.strip(" :-") \
                                for content in re.split(r"[|｜]", raw_line)]
                            assert len(contents) >= len(headers), \
                                f"Check MD line: {raw_line}"
                            contents = contents[1:len(headers)+1]
                            if all(len(content)==0 for content in contents):
                                skip_write = True
                            else:
                                # table contents
                                leads_names = [name.strip(" ") \
                                    for name in contents]
                                for name in leads_names:
                                    out_fp.write(name + "\n")
                                skip_write = True
                        else:
                            if len(matched.group(0)) > 0:
                                # table header
                                is_processing_table = True
                                headers = [header.strip(" ") \
                                    for header in re.split(r"[|｜]", raw_line)]
                                assert len(headers) >= 2, \
                                    f"Check MD line: {raw_line}"
                                headers = headers[1:3]
                                skip_write = True
                    elif 1101 <= id_num <= 1299:
                        if is_processing_table:
                            assert len(headers) > 0, \
                                f"Check MD line: {raw_line}"
                            contents = [content.strip(" :-") \
                                for content in re.split(r"[|｜]", raw_line)]
                            len_contents = len(headers) + 1
                            contents = contents[1:len_contents]
                            if all(len(content)==0 for content in contents):
                                skip_write = True
                            else:
                                # table contents
                                two_lines = compile_two_lines(headers,
                                    contents, raw_line)
                                out_fp.write(two_lines[0] + "\n")
                                out_fp.write(two_lines[1] + "\n")
                                skip_write = True
                        else:
                            if len(matched.group(0)) > 0:
                                # table header
                                is_processing_table = True
                                headers = [header.strip(" ") \
                                    for header in re.split(r"[|｜]", raw_line)]
                                len_headers = 5 if id_num == 1204 else 6
                                if headers[-1] == "":
                                    len_headers -= 1
                                assert len_headers >= 4, "".join(
                                    ["ERR: ASV Plugin:len_headers >= 4, ",
                                    f"but it's {len_headers}"])
                                headers = headers[1:len_headers]
                                skip_write = True
                else:
                    is_processing_table = False
                    headers = []
                    skip_write = False
                if not skip_write:
                    out_fp.write(raw_line_orig)

    shutil.copyfile(convered_path, markdown_path)
    return markdown_path


def _test():

    def get_cust_styles(lang):
        return {}

    dont_care:str = ""
    my_proj_path = os.getcwd()
    data_dir_path = Path(os.path.join(my_proj_path, "owasp_pdf_data_ASV"))
    proj_def_generator = register_project("ASV", ("en-US",),
        data_dir_path, dont_care, get_cust_styles)
    for proj_def in proj_def_generator:
        assert proj_def["proj_code"] == "ASV"
        assert proj_def["lang"] == "en-US"
        assert proj_def["proj_dir"] == "asv"
        assert isinstance(proj_def["styles"], dict)
    print("Test: success!!")

if __name__ == '__main__':
    _test()
