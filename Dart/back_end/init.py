from db.models import StdDisc

def init():
    init_models()

def init_models():
    return
    if StdDisc.objects.count() > 0:
        return

    # 1.지분공시
    StdDisc(1, '임원ㆍ주요주주특정증권등소유상황보고서').save()
    StdDisc(2, '주식등의대량보유상황보고서').save()
    StdDisc(3, '공개매수신고서').save()

    # 2.주요사항보고
    StdDisc(4, '자기주식취득결정').save()
    StdDisc(5, '자기주식취득신탁계약체결결정').save()
    StdDisc(6, '타법인주식 및 출자증권 취득/처분/양수/양도 결정').save()
    StdDisc(7, '유상/무상증자 결정').save()
    StdDisc(8, '감자결정').save()
    StdDisc(9, '전환사채권 발행결정').save()
    StdDisc(10, '주권관련 사채권 양도/양수 결정').save()
    StdDisc(11, '회사 분할/합병 결정').save()
    StdDisc(12, '유형자산 양수/양도 결정').save()
    StdDisc(13, '영업 양수/양도 결정').save()
    StdDisc(14, '신주인수권부사채권발행결정').save()
    StdDisc(15, '교환사채권발행결정').save()

    # 3.정기공시
    StdDisc(16, '사업보고서').save()
    StdDisc(17, '분기보고서').save()
    StdDisc(18, '반기보고서').save()

    # 4.거래소 공시
    StdDisc(19, '단일판매ㆍ공급계약체결').save()
    StdDisc(20, '최대주주등 소유주식 변동 신고서').save()
    StdDisc(21, '감사보고서 제출').save()
    StdDisc(22, '자산재평가').save()

    StdDisc(23, '조회공시').save()
    StdDisc(24, '최대주주변경').save()


