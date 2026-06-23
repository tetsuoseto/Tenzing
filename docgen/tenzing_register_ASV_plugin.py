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
        "doc_template_type": "blank",
        "doc_title_pivot.pt_x": 306,
        "doc_title_pivot.pt_y": 250,
        "doc_toc_title_pivot.pt_x": 306,
        "doc_toc_title_pivot.pt_y": 80, # add 15 for bi-di for optimal result
        "doc_header": " ",
        "doc_header_pivot.pt_x": 72,
        "doc_header_pivot.pt_y": 30,
        "doc_legal_notice": False,
        "doc_title_font.size": 30,
        "doc_title_font.line_pitch": 45,
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
        "doc_appendix_title_font.size": 13.0,
        "doc_appendix_title_font.line_pitch": 18.2,
        "doc_appendix_title_font.line_alignment": "left",
        "doc_appendix_title_font.color": "black",
        "header_font.color": "white",
        "chapter_pivot.pt_x": 72,
        "chapter_pivot.pt_y": 72,
        "chapter_title_bottom_aligned": False,
        "chapter_font.size": 24,
        "chapter_font.line_pitch": 28,
        "chapter_font.line_alignment": "left",
        "chapter_font.color": "black",
        "section_font.size": 16,
        "section_font.line_pitch": 18.2,
        "caption_font.size": 0.1,
        "caption_font.line_pitch": 0.0,
        "caption_font.line_alignment": "left",
        "caption_font.color": "white",
        "blockquote_font.size": 10.0,
        "blockquote_font.line_pitch": 14.0,
        "blockquote_font.line_alignment": "justified",
        "reference_font.size": 10.0,
        "reference_font.line_pitch": 14.0,
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
        "Security Verification Standard"
    ]
    cs["doc_subtitles"] = [
        "",
        "Initial Version Work In Progress",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "_______ ___, 2026"
    ]
    cs["doc_revision_history"] = [
        "    2026-__-__  1.0  English Version Release",
    ]
    cs["doc_toc_contents_title"] = "Table of Contents"
    cs["doc_toc_figures_title"] = "Figures and Tables"
    cs["doc_toc_translations"] = [
        "Table:Table", "Figure:Figure", "Control:Control"]
    cs["doc_appendix_titles"] = []
    cs["doc_sponsor_page_titles"] = []
    if lang in ("ar-SA", "he-IL", "fa-IR"):
        cs["doc_toc_title_font.line_alignment"] = "right"
        cs["chapter_font.line_alignment"] = "right"
        cs["caption_font.line_alignment"] = "right"
        cs["reference_font.line_alignment"] = "right"
    else:
        cs["doc_toc_title_font.line_alignment"] = "left"
        cs["chapter_font.line_alignment"] = "left"
        cs["caption_font.line_alignment"] = "left"
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
# data_dir_path: full path to data directory "tenzing_data_OLM"
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
        temp_dir_path: str, doc_toc_translations: list):
    # pylint: disable=too-many-statements, too-many-branches, too-many-locals
    assert proj_code == "ASV"
    str_control: str = "Control"
    for trans_pair in doc_toc_translations:
        items = trans_pair.split(":")
        if items[0] == str_control:
            str_control = items[1]
            break

    def compile_three_lines(headers: List[str], contents: List[str],
            raw_line: str, id_num: int):
        assert len(headers) == len(contents), \
            f"Check MD line: {raw_line}"
        level: int = 0
        level_str: str = "TRANS ERR"
        line0: str = ""
        line1: str = ""
        line2: str = ""
        try:
            level = int(contents[2])
            level_str = str(level)
            level_colors = LEVEL_COLORS.get(level, DFLT_LEVEL_COLORS)
        except Exception:
            level_colors = DFLT_LEVEL_COLORS
        if id_num==1002 and len(headers) == 3:
            # id_num==1002 : | Column | Meaning |
            line1 = ">"+level_colors[0]+"|black||||hb  "+\
                headers[0].replace(" ","")+" : "+contents[0].strip("*")
            line2 = ">"+level_colors[1]+"|black  "+\
                "    "+contents[1]
        elif id_num==1201 and len(headers) == 3:
            # id_num==1203 : | Control / Technique | Requirement IDs |
            # Option 1: use blockquote
            #   Pros: multiline is supported (not broken)
            #   Cons: not shown on TOC (okay)
            line1 = ">white|black||||hb  "+\
                headers[0].replace(" ","")+" : "+contents[0].strip("*")
            # Option 2: use ###$
            #   Pros: shown on TOC with back link (broken)
            #   Cons: long line goes beyond margin (maybe good/maybe noisy)
            # line1 = "###$ " + contents[0].strip("*")
            line2 = "     "
            added_to_line2: bool = False
            content_items = contents[1].split(",")
            for content_item in content_items:
                if added_to_line2:
                    line2 += ", "
                content_item_stripped = content_item.strip()
                if content_item_stripped[0] == "C":
                    content_item_stripped = content_item_stripped[1:]
                line2 += str_control+" "+content_item_stripped
                added_to_line2 = True
        else:
            if headers[0] == "#":
                # add caption in white color and thin pitch
                line0 = "####@ "+str_control+" "+\
                    contents[0].strip("*")+": ("+ \
                    headers[2]+" "+contents[2]+")"
            line1 = ">"+level_colors[0]+"|black||||hb  "+\
                headers[0]+contents[0]
            line2 = ">"+level_colors[1]+"|black  "+contents[1]
            if len(headers) == 4:
                line1 += ("    "+headers[2]+": "+level_str)
                line2 = "  >"+level_colors[1]+"|black  "+contents[1]
            # this line needed for old Appendix chapter?
            # line1 += ("    "+headers[-1]+": "+str(contents[-1]))
        return line0, line1, line2

    def compile_three_lines_1003(headers: List[str], contents: List[str],
            raw_line: str, id_num: int):
        assert id_num == 1003, \
            f"Check MD line: {raw_line}"
        assert len(headers) == len(contents), \
            f"Check MD line: {raw_line}"
        level0: int = 0
        level1: int = 0
        use_str: str = "TRANS ERR"
        line0: str = ""
        line1: str = ""
        line2: str = ""
        try:
            level0 = int(contents[0])
            level_colors = LEVEL_COLORS.get(level0, DFLT_LEVEL_COLORS)
            level1 = int(contents[1])
            use_str = str(contents[2])
        except Exception:
            return use_str, use_str, use_str
        line0 = f">{level_colors[0]}|||||hb  {headers[0]} " + \
            f"{str(level0)}  =  {headers[1]} {str(level1)}"
        line1 = f"  >|||||bb  {headers[2]}:"
        line2 = f"  >|||||br  {use_str}"
        return line0, line1, line2

    re_sharp = "^([\\#]+[@\\$]{0,1})( .*)$"
    re_exclam = "^(\\!\\[)(.*)$"
    re_bar = "^[\\|｜][^\\|｜].*$"
    re_id_num = f"^{proj_code}([0-9]+)_"
    re_special_color = r"^[#]{4}.+([1-3一二三])"
    re_glossary = r"^\* (.+) [-–]{1} (.+)$"
    # Note: the second – is 0x2013, not the regular hyphen.

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
                if raw_line.startswith("<!--"): # html comment line
                    continue
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

                # rich glossary formatting
                #-----------------------
                if id_num == 1200:
                    matched = re.match(re_glossary, raw_line)
                    if matched:
                        glossary_term: str = matched.group(1)
                        out_str = f">|||||bb {glossary_term}" + "\n"
                        out_fp.write(out_str)
                        glossary_desc: str = matched.group(2)
                        out_str = f"  >|||||br {glossary_desc}" + "\n"
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
                    raw_line = "#" + matched.group(1) + matched.group(2) + "\n"
                    out_fp.write(raw_line)
                    continue
                # image directory adjustment
                #-----------------------
                # from "../images/license.png" to "images/license.png"
                # Does the line start with "!"?
                matched = re.match(re_exclam, raw_line)
                if matched:
                    raw_line = raw_line.replace("../images", "images") + "\n"
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
                                headers = headers[1:-1]
                                skip_write = True
                    elif id_num == 1003:
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
                                three_lines = compile_three_lines_1003(headers,
                                    contents, raw_line, id_num)
                                out_fp.write(three_lines[0] + "\n")
                                out_fp.write(three_lines[1] + "\n")
                                out_fp.write(three_lines[2] + "\n")
                                skip_write = True
                        else:
                            if len(matched.group(0)) > 0:
                                # table header
                                is_processing_table = True
                                headers = [header.strip(" ") \
                                    for header in re.split(r"[|｜]", raw_line)]
                                headers = headers[1:-1]
                                skip_write = True
                    elif id_num == 1002 or (1101 <= id_num <= 1299):
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
                                three_lines = compile_three_lines(headers,
                                    contents, raw_line, id_num)
                                out_fp.write(three_lines[1] + "\n")
                                if three_lines[0]:
                                    # insert hidden caption line in between
                                    # with caption_font.line_pitch == 0.0,
                                    # which guarantees the caption is printed
                                    # in the same page as the first line.
                                    # set caption_font.size to 0.1.
                                    out_fp.write(three_lines[0] + "\n")
                                out_fp.write(three_lines[2] + "\n")
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
    data_dir_path = Path(os.path.join(my_proj_path, "tenzing_data_ASV"))
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
