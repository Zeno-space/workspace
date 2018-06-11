import re
# s = 'Alex li'
# s1 = 'staff_table Alex Li,25,13443534411,IT,2015-10-29'
# s3 = '2013‐04‐01'
# p4 = r'(\d{4}-\d{2}-\d{2})'
# pattern = ' /^[\u4E00-\u9FA5\uf900-\ufa2d·s]{2,20}$'
# p1 = '([a-zA-Z\s]+),'  # 可以
# p2 = '([a-zA-Z]+\s*){1,2},'
# p3 = 'staff_table\s+([a-zA-Z\s]+),(\d+),(\d{11}),([a-zA-Z]+),(\d{4}-\d{1,2}‐\d{1,2})'  # 可以
# p2_name = '^[/u4e00-/u9fa5]{2,5}|(^[a-zA-Z]+[/s.]?{0,4})'
# p3_name = r'^[a-zA-Z]+[\s.]?{0,4}'

# s9 = 'staff_table Alex Li,25,13443534411,IT,2015‐10-29'
# p9 = r'staff_table\s+([a-zA-Z\s]+),(\d+),(\d{11}),([a-zA-Z]+),(\d{4}-\d{1,2}-\d{1,2})'

# s10 = '2013-04-01'
# p10 = r'(\d{4}-\d{1,2}-\d{1,2})'
# result = re.match(p3, s1, re.U).groups()
# print(result)
# print('‐'.encode('gbk'))
# print('-'.encode('gbk'))


# (?aiLmsux) Set the A, I, L, M, S, U, or X flag for the RE (see below).
# (?:...)  Non-grouping version of regular parentheses.
# (?P<name>...) The substring matched by the group is accessible by name.
# (?P=name)     Matches the text matched earlier by the group named name.
# (?#...)  A comment; ignored.
# (?=...)  Matches if ... matches next, but doesn't consume the string.
# (?!...)  Matches if ... doesn't match next.
# (?<=...) Matches if preceded by ... (must be fixed length).
# (?<!...) Matches if not preceded by ... (must be fixed length).
# (?(id/name)yes|no) Matches yes pattern if the group with id/name matched,
#                 the (optional) no pattern otherwise.
result = re.match('.+\.(?=ba+$).+', 'a.bac')
# result = re.match('.+\.[^(bat)]', 'a.tac')    #不能排除.bat
print(result)
