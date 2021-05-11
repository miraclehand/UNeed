from db.models import MetaData, Version, StdDisc
from commons.utils.datetime import str_to_datetime

def init():
    init_meta_data()
    init_version()
    init_std_disc()

def init_meta_data():
    if MetaData.objects.count() > 0:
        return

    version = '2020.01.01.001'
    MetaData(version, version).save()

def init_version():
    if Version.objects.count() > 0:
        return

    date = str_to_datetime('20200101', '%Y%m%d')
    Version(date, date).save()
    
def init_std_disc():
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

    """
    # 1.지분공시
    StdDisc(000, '전체').save()
    StdDisc(100, '임원ㆍ주요주주특정증권등소유상황보고서').save()
    StdDisc(101, '주식등의대량보유상황보고서').save()
    StdDisc(102, '공개매수', '공개매수 신고서/보고서').save()

    # 2.주요사항보고
    StdDisc(200, '자기주식', '자기주식 취득/계약/처분').save()

    StdDisc(202, '타법인주식및출자증권', '타법인주식 및 출자증권 취득/처분/양수/양도 결정').save()
    StdDisc(203, '상증자', '유상/무상증자 결정').save()
    StdDisc(204, '감자결정|감자완료', '감자 결정/완료').save()
    StdDisc(205, '전환사채', '전환사채권 발행 결정').save()
    StdDisc(206, '상장채권|매출채권|사채권|채권은행','주권관련 사채권 취득/양도/양수 결정').save()
    StdDisc(207, '배당결정', '현금ㆍ현물배당결정').save()
    StdDisc(208, '회사분할|회사합병', '회사 분할/합병 결정').save()
    StdDisc(209, '유형자산', '유형자산 양수/양도 결정').save()

    StdDisc(210, '영업양수|영업양도|자산양수|자산양도', '자산 양수/양도 결정').save()
    StdDisc(211, '신주인수권', '신주인수권부사채권발행/ 조정').save()
    StdDisc(212, '교환사채권발행결정').save()
    StdDisc(213, '타인에대한채무보증결정').save()
    # 3.정기공시
    StdDisc(300, '사업보고서').save()
    StdDisc(301, '분기보고서').save()
    StdDisc(302, '반기보고서').save()

    # 4.거래소 공시
    StdDisc(400, '단일판매ㆍ공급계약', '단일판매ㆍ공급계약 체결/해지').save()
    StdDisc(401, '최대주주등소유주식변동|최대주주등의주식보유변동',  '최대주주등 소유주식 변동').save()
    StdDisc(402, '감사보고서', '감사보고서 제출').save()
    StdDisc(403, '자산재평가').save()

    StdDisc(500, '조회공시').save()
    StdDisc(501, '최대주주변경').save()
    StdDisc(502, '특수관계인', '특수관계인과의 거래').save()
    StdDisc(503, '자본잠식').save()
    StdDisc(504, '검찰|소송|횡령|배임|벌금', '검찰 기소/고발 혹은 횡령/배임/소송 공시').save()
    StdDisc(505, '기업인수목적회사', '기업인수목적회사 공시').save()
    StdDisc(506, '부동산투자회사', '부동산투자회사 공시').save()
    StdDisc(507, '선박투자회사', '선박투자회사 공시').save()
    StdDisc(508, '유동성공급계약', '유동성공급계약의 체결/변경/해지').save()
    StdDisc(509, '주주총회', '주주총회 소집/결과').save()
    StdDisc(510, '파산|부도', '파산/부도 공시').save()
    StdDisc(511, '기술도입', '기술도입 공시').save()
    StdDisc(512, '단기차입금', '단기차입금 증가/감소').save()
    StdDisc(514, '불성실공시', '불성실공시법인 지정/미지정').save()
    StdDisc(515, '거래정지', '주권/은행 거래정지').save()
    StdDisc(516, '회생절차|회생계획', '회생 절차/계획').save()
    StdDisc(517, '생산중단|생산재개', '생산 중단/재개').save()
    StdDisc(518, '타법인주식및출자증권', '타법인주식및출자증권 양수/양도').save()
    StdDisc(519, '지주회사의자회사', '지주회사의 자회사 편입/탈퇴').save()
    StdDisc(520, '경영사항').save()
    StdDisc(521, '풍문또는보도에대한해명').save()
    StdDisc(522, '대표이사변경|대표이사(대표집행임원)변경', '대표이사변경').save()
    StdDisc(523, '투자설명서').save()
    StdDisc(524, '증권신고서').save()
    StdDisc(525, '증권발행실적보고서').save()
    StdDisc(526, '일괄신고', '일괄신고서').save()
    StdDisc(527, '합병등종료보고서').save()
    StdDisc(528, '영업실적|영업(잠정)실적|결산실적|공모실적', '영업실적 및 전망').save()
    StdDisc(529, '파생상품거래', '파생상품거래 이익/손실').save()
    StdDisc(530, '자원개발', '자원개발 투자/진행').save()
    StdDisc(531, '신탁계약', '신탁계약 취득/해지').save()
    StdDisc(532, '상각형조건부자본증권발행결정').save()
    StdDisc(533, '지속가능경영보고서등관련사항').save()
    StdDisc(534, '사외이사의선임', '사외이사의선임ㆍ해임또는중도퇴임에관한신고').save()
    StdDisc(535, '주식소각', '주식소각결정').save()
    StdDisc(536, '기업설명회', '기업설명회(IR)개최').save()
    StdDisc(537, '주식매수선택권', '주식매수선택권 행사').save()
    StdDisc(538, '상장폐지', '상장폐지 결정').save()
    StdDisc(539, '계열회사|계열금융회사', '계열회사와의 거래').save()
    StdDisc(540, '시설투자|시설외투자', '시설/시설외 투자').save()
    StdDisc(541, '외부감사인선임', '외부감사인 선임/해임').save()
    StdDisc(542, '해외증권').save()
    StdDisc(543, '타인에대한담보제공결정').save()
    StdDisc(544, '의결권대리행사권유', '의결권대리행사권유').save()
    StdDisc(545, '전환청구권행사').save()
    StdDisc(546, '매출액또는손익구조').save()
    StdDisc(547, '본점소재지변경').save()
    StdDisc(548, '기타시장안내').save()
    StdDisc(549, '전환가액', '전환가액의조정').save()
    StdDisc(550, '증권발행결과').save()
    StdDisc(551, '투자유의안내').save()
    StdDisc(552, '주식분할결정').save()
    StdDisc(553, '교환청구권행사').save()
    StdDisc(554, '주주명부폐쇄').save()
    StdDisc(555, '지정자문인선임계약','지정자문인 선임계약의 체결/해지').save()
    StdDisc(556, '소속부변경').save()
    StdDisc(557, '기타안내사항').save()
    StdDisc(558, '금전대여|증권대여', '금전/증권대여 결정).save()
    StdDisc(559, '영업정지', '영업정지').save()
    StdDisc(560, '주식교환|주식병합', '주식 병합/교환 결정').save()
    StdDisc(561, '기업지배구조보고서공시').save()
    StdDisc(562, '거래처와의거래중단').save()
    StdDisc(563, '수시공시의무관련사항').save()
    StdDisc(564, '공정거래자율준수프로그램운영현황').save()
    StdDisc(565, '해산사유발생').save()
    StdDisc(566, '장래사업ㆍ경영계획').save()
    StdDisc(567, '교환사채(해외교환사채포함)발행후만기전사채취득').save()
    StdDisc(568, '경영권변경등에관한계약체결').save()
    StdDisc(569, '대표집행임원변경').save()
    StdDisc(570, '소액공모', '소액공모공시').save()
    StdDisc(571, '상호변경안내').save()
    StdDisc(572, 'CB발행결정철회').save()
    StdDisc(573, '중요한자산양수도결정').save()
    StdDisc(574, '교환가액의조정').save()
    StdDisc(575, '채무인수결정').save()
    StdDisc(576, '철회신고서').save()
    StdDisc(577, '선급금지급결정').save()
    StdDisc(578, '대규모기업집단현황공시').save()
    StdDisc(579, '대출원리금연체사실발생').save()
    StdDisc(580, '재해발생').save()
    StdDisc(591, '임원의변동').save()
    StdDisc(592, '감사전재무제표기한내미제출신고서').save()
    StdDisc(593, '배당락').save()
    StdDisc(594, '회계처리기준위반에따른임원의해임권고조치').save()
    StdDisc(595, '이사회의성별구성의무준수현황').save()
    StdDisc(596, '사채원리금미지급발생').save()
    StdDisc(597, '경영정상화계획의이행약정체결').save()
    StdDisc(598, '채무면제결정').save()
    StdDisc(599, '결산기변경안내').save()
    StdDisc(600, '특허권취득').save()
    StdDisc(601, '이전상장결정').save()
    StdDisc(602, '풋백옵션등계약체결결정').save()
    StdDisc(603, '가족친화인증ㆍ유효기간연장ㆍ인증취소').save()
    StdDisc(604, '반기검토의견부적정또는의견거절').save()
    StdDisc(605, '비유동자산취득결정').save()
    StdDisc(606, '주요주주변경').save()
    StdDisc(607, '종류주식의보통주식으로전환결의').save()
    StdDisc(608, '임상시험단계진입ㆍ종료').save()
    StdDisc(609, '녹색기업|녹색기술', '녹색/기술 사업에대한인증ㆍ취소').save()
    StdDisc(610, '어음위ㆍ변조발생').save()
    StdDisc(611, '제품에대한수거ㆍ파기등결정').save()
    StdDisc(612, '수증').save()
    StdDisc(613, '증권예탁증권(DR)발행결정').save()
    StdDisc(614, '소액공모법인결산서류').save()
    StdDisc(615, '증여결정').save()
    StdDisc(615, '온실가스배출권의처분').save()
    
    



    
    """



    """
    StdDisc.objects.raw({
    '$where': 'function() { \
            return this.report_nm.match(\'' + report_nm + '\' ) \
                }'
                }).first()
    """

    """
    StdDisc.objects.raw({
    '$where': 'function() { \
            return "자기주식취득결정했지롱".match(this.report_nm) \
                }'
    }).first()
    """


    """
    STD_DISC 변경

    1. std_disc 삭제
    2. db.models  STD_DISC 수정
    3. init.py 재생성, 일자변경
    4. Disc에 std_disc 재 할당
    5. ChatRoom

    6. UserWatch(Unit)  => UserWatch(MongoModel)
    watchs 안에 Unit 있다. 거기에 StdDisc 사용함
    7. UserSimula(Unit) => UserSimula(MongoModel)
    simuas 안에 Unit 있다. 거기에 StdDisc 사용함

    8. Disc안에 StdDisc 있다

    email = 'minkyu8306@gmail.com'
    user = User.objects.get({'email':email})
    uw = UserWatch.objects.get({'user':user._id})
    uw.watchs.__len__()

    watchs[0]: ObjectId('607ffbac36b367817e313a35')   id: 7    -> 203
    watchs[1]: ObjectId('6080ce1d0132a0a344e02b06')   id: 19   -> 400
    watchs[2]: ObjectId('6080cdeb0132a0a344e02b05')   id: 11   -> 208

    """
    """                                                     
    from db.models import StdDisc, Disc
    _std_disc = dict()
    discs = Disc.objects.raw({})
    for disc in discs:
        f = 0
        for keyword in keywords:
            for k in keyword.split('|'):
                if disc.report_nm.find(k) >= 0:
                    f = 1
        if f == 0:
            print(disc.report_nm)

    """                                                     

    """
    import sys
    sys.path.append('../../')
    from db.models import Disc
    import requests
    import time
    from task.reportparser import report_2
    discs = Disc.objects.raw({'rcept_dt':{'$gte':'20170101','$lte':'20171231'}}).order_by([('rcept_dt',1)])
    f = 0
    for disc in discs:
        if disc.report_nm.find('상증자결정') < 0:
            continue
        if disc.report_nm.find('무') < 0:
            continue
        if disc.report_nm.find('첨부정정') >= 0:
            continue
        f = f + 1
        print(disc.report_nm, disc.url)
        html = requests.get(disc.url).text
        disc.content = report_2(html)
        if not disc.content:
            disc.content = disc.report_nm
        disc.save()
        print(disc.content)
        time.sleep(20)
    """

