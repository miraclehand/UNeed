import requests
from task.parser import elim_tag

# 단일판매 공급계약체결
def report_1(html):
    trs = html.split('<tr>')

    l, a, r = '<', '</', '>'
    content= ''
    content= content+' * 계약내용:'+elim_tag(trs[1].split('<td')[2],l,a,r)+'\n'
    content= content+' * 계약상대:'+elim_tag(trs[8].split('<td')[2],l,a,r)+'\n'
    content= content+' * 계약금액:'+elim_tag(trs[5].split('<td')[2],l,a,r)+'\n'
    content= content+' * 최근매출:'+elim_tag(trs[6].split('<td')[2],l,a,r)+'\n'
    content= content+' * 매출대비:'+elim_tag(trs[7].split('<td')[2],l,a,r)+'\n'
    content= content+' * 연환산:'+''+'\n'
    content= content+' * 계약시작:'+elim_tag(trs[14].split('<td')[3],l,a,r)+'\n'
    content= content+' * 계약종료:'+elim_tag(trs[15].split('<td')[2],l,a,r)
    """
        #1. 판매 공급계약 구분
        #   - 세부내용
        #2. 계약내역
        #   - 계약금액(원)
        #   - 최근매출액(원)
        #   - 매출액대비(%)
        #   - 대규모법인여부
        #3. 계악상대
        #   - 회사와의 관계
        #4. 판매 공급지역
        #5. 계약기간
        #   - 시작일
        #   - 종료일
        #6. 주요 계약조건
        #7. 계약(수주)일
        #8. 기타 투자판단과 관련한 주요사항
    """

    return content
