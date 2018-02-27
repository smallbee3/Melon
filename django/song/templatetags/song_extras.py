from django import template

register = template.Library()


# 방법 1
# @register.filter(name='ellipsis_line')
def ellipsis_line(value, arg):

    # value로부터
    # arg에 주어진 line수만큼의
    # 문열(Line)을 반환
    # 만약 arg의 line수보다
    #   value의 line이 많으면
    #   마지막에 ...추가

    #
    lines = value.splitlines() # 얘를 쓰면 리스트 형태로 구분이감. 배열안에 한줄씩.

    # 리스트의 길이가 주어진 arg(line수) 보다 길 경우
    if len(lines) > arg:
        # 줄바꿈 문자 단위로
        # multi-line string을 분할한 리스트를
        #   arg(line수)개수까지 슬라이싱한 결과를 합칩
        #   마지막 요소에는 '...'을 추가
        return '\n'.join(lines[:arg + 1] + ['...'])

    return value


# 방법 2
register.filter('ellipsis_line', ellipsis_line)
