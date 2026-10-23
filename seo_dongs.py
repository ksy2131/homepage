# -*- coding: utf-8 -*-
# 읍면동별 전기수리 페이지 — build_site.py 안에서 exec로 불러 씀 (LOCALS 확장, build_local 교체)
# 동네 데이터는 dong_data.py (DONG_DATA). 문장 안의 {n}은 동네 이름으로 바뀝니다.

# ───────────── 동네 성격별 정보성 주제 (동네마다 1~2개 배정) ─────────────
TOPICS = {
 "panel_age": {
  "title": "{n} 25년 넘은 아파트·빌라·상가, 분전반·차단기 교체 시기 확인하기",
  "paras": ["{n}처럼 1990년대에 지어진 아파트·빌라·상가 건물은 분전반(두꺼비집)과 차단기도 건물과 같은 나이입니다. 차단기는 수명이 다하면 정상 전류에서도 떨어지거나, 반대로 떨어져야 할 때 안 떨어집니다. 겉보기에 멀쩡해도 손잡이가 헐겁거나 누렇게 변색됐다면 교체를 생각할 시기입니다.",
            "분전반 전체를 바꿀지, 문제 차단기만 바꿀지는 상태를 보고 정합니다. 교체할 때 인덕션·에어컨 회로를 따로 나누면 차단기 떨어짐 문제도 같이 해결됩니다."],
  "head": ["설비", "점검·교체를 생각할 시기", "이런 신호가 보이면 교체"],
  "rows": [["누전차단기(메인)", "15~20년", "시험버튼을 눌러도 안 떨어짐, 이유 없이 자주 떨어짐"],
           ["분기 차단기", "20년 전후", "손잡이가 헐거움, 변색, 올려도 바로 떨어짐"],
           ["분전반 함체·단자", "25년 이상", "단자 변색·탄 냄새, 차단기 추가할 자리 없음"],
           ["세대 배선(전선)", "30년 전후 점검", "절연저항 측정값이 낮음, 콘센트 여러 곳 발열"]],
  "cap": "교체 시기는 사용 환경에 따라 다르며, 측정으로 상태를 확인한 뒤 결정합니다.",
  "guide": "guide-panel-replace"},
 "old_outlet": {
  "title": "{n} 오래된 집 콘센트·스위치, 한 번에 바꿔야 할까?",
  "paras": ["{n}의 오래된 주택·아파트는 콘센트 안쪽 접점이 닳아 플러그가 헐겁게 꽂히는 경우가 많습니다. 헐겁게 꽂히면 접촉 면적이 줄어 열이 나고, 그을음과 탄 냄새로 이어집니다.",
            "한두 개만 문제라면 그것만 바꾸면 되지만, 같은 시기에 단 콘센트가 여러 개 헐겁다면 집 전체를 한 번에 교체하는 편이 출장 횟수와 비용을 줄입니다. 교체하면서 뒤쪽 전선 접속부까지 다시 조여 둡니다."],
  "head": ["증상", "원인", "권장 작업"],
  "rows": [["플러그가 헐겁게 꽂힘", "콘센트 접점 마모", "콘센트 교체"],
           ["콘센트 주변 그을음·탄 냄새", "접촉 불량으로 발열", "즉시 사용 중지, 교체 및 접속부 재시공"],
           ["스위치를 여러 번 눌러야 켜짐", "스위치 접점 노후", "스위치 교체"],
           ["스위치·콘센트 커버 누렇게 변색", "오랜 사용·열", "상태 확인 후 일괄 교체 검토"]],
  "cap": "",
  "guide": "guide-outlet-burn"},
 "fluorescent": {
  "title": "{n} 형광등을 LED로 바꿀 때 알아둘 것",
  "paras": ["{n}에서 가장 흔한 조명 문의는 오래된 형광등이 깜빡이거나 안 켜지는 경우입니다. 형광등은 램프만 바꿔도 안정기가 낡으면 금방 다시 고장 납니다.",
            "형광등 등기구에 LED 램프만 끼우는 방법도 있지만, 안정기를 그대로 두면 안정기 고장이 반복될 수 있어 등기구째 LED로 바꾸는 경우가 많습니다. 천장 배선 상태도 이때 같이 확인합니다."],
  "head": ["항목", "형광등", "LED 등기구"],
  "rows": [["같은 밝기 소비전력", "높음", "낮음 (보통 절반 안팎)"],
           ["자주 고장 나는 부품", "램프, 안정기", "LED 모듈, 컨버터"],
           ["깜빡임", "안정기 노후 시 잦음", "컨버터 고장 시 발생"],
           ["교체 방법", "램프·안정기 교체", "등기구 일체 교체가 일반적"]],
  "cap": "소비전력 차이는 제품마다 다릅니다.",
  "guide": "guide-led-light"},
 "new_circuit": {
  "title": "{n} 신축 아파트, 입주 후 인덕션·건조기 전용 회로가 필요한 이유",
  "paras": ["{n} 신축 단지에서 가장 많이 받는 문의는 입주 후 인덕션·식기세척기·건조기를 들이고 나서 주방 차단기가 떨어지는 경우입니다. 분양 당시 주방 콘센트 회로 하나에 여러 가전을 같이 쓰도록 되어 있는 경우가 많기 때문입니다.",
            "큰 가전은 전용 회로(분전반에서 그 기기까지 따로 빼는 선)를 두면 차단기 떨어짐이 사라집니다. 분전반에 빈 자리가 있으면 공사가 간단합니다."],
  "head": ["가전", "대략 소비전력", "전용 회로 권장"],
  "rows": [["인덕션(3구)", "3~4kW 안팎", "필요"],
           ["전기건조기", "2~3kW 안팎", "권장"],
           ["식기세척기", "1.5~2kW 안팎", "권장 (인덕션과 같은 회로 X)"],
           ["시스템 에어컨 실외기", "제품별 상이", "보통 입주 때 별도 회로"],
           ["전자레인지·전기포트", "1~1.5kW 안팎", "같이 켜면 과부하 주의"]],
  "cap": "소비전력은 제품 표시를 기준으로 확인합니다.",
  "guide": "guide-breaker-trips"},
 "led_module": {
  "title": "{n} 입주 5~10년 차, LED 방등이 하나둘 고장 나는 이유",
  "paras": ["{n}처럼 2010년대에 입주한 단지는 입주 때 달린 LED 방등·거실등이 하나둘 고장 나기 시작하는 시기입니다. 일부만 어둡거나, 깜빡이다가 아예 안 켜지는 증상이 대표적입니다.",
            "LED 등은 빛을 내는 모듈과 전원을 바꿔 주는 컨버터(안정기)로 나뉩니다. 어느 쪽이 고장인지에 따라 부품만 바꿀지, 등 전체를 바꿀지가 갈립니다. 같은 시기에 단 등이라면 다른 방 등도 비슷한 시기에 고장 나는 경우가 많습니다."],
  "head": ["증상", "의심 부품", "조치"],
  "rows": [["일부 칩만 어두움, 얼룩덜룩함", "LED 모듈", "모듈 교체 또는 등 교체"],
           ["깜빡이다가 안 켜짐", "컨버터", "컨버터 교체"],
           ["스위치를 꺼도 희미하게 켜짐", "스위치·배선 잔류전압", "스위치·배선 확인"],
           ["새 등으로 바꿔도 안 켜짐", "스위치 또는 천장 배선", "전압 측정 후 정비"]],
  "cap": "",
  "guide": "guide-led-light"},
 "kitchen_leak": {
  "title": "{n} 아파트 주방·아일랜드 콘센트 누전, 왜 자꾸 생길까?",
  "paras": ["{n} 단지에서 누전으로 차단기가 떨어지는 경우, 원인을 찾아 들어가면 주방 싱크대 하부나 아일랜드 식탁에 붙은 콘센트인 경우가 많습니다. 물을 쓰는 곳 바로 옆이라 습기와 물방울이 콘센트 안으로 들어가기 쉽습니다.",
            "정수기·식기세척기·음식물처리기가 싱크대 하부 콘센트를 같이 쓰는 경우가 많아, 기기 하나만 젖어도 주방 전체 회로가 떨어집니다. 기기를 하나씩 분리해 측정하면 원인을 금방 찾습니다."],
  "head": ["위치", "자주 생기는 문제", "예방·조치"],
  "rows": [["싱크대 하부 콘센트", "습기·누수로 누전", "물 닿지 않는 위치로 이설, 방수형 콘센트"],
           ["아일랜드 식탁 콘센트", "물 튐, 탄 자국", "덮개 있는 콘센트로 교체"],
           ["정수기·음식물처리기", "기기 내부 누전", "기기 분리 측정 후 수리 요청"],
           ["베란다 세탁기 콘센트", "결로·습기", "접지 확인, 방수형 교체"]],
  "cap": "",
  "guide": "guide-leakage-check"},
 "shop": {
  "title": "{n} 상가·매장 전기, 영업 중 정전을 막으려면",
  "paras": ["{n}처럼 상가가 몰린 곳은 매장 전기 문의가 많습니다. 매장은 냉장·냉동 쇼케이스, 커피머신, 전기그릴, 간판까지 한꺼번에 돌아가기 때문에 차단기 하나가 떨어지면 영업이 멈춥니다.",
            "업종을 바꾸며 기기를 추가했는데 분전반은 예전 그대로인 경우가 흔합니다. 매장 분전반에서 회로별 사용 전류를 재 보면 어느 회로가 한계에 가까운지 보이고, 필요한 회로만 증설하면 됩니다. 영업 시간을 피해 작업 일정을 잡습니다."],
  "head": ["업종", "전기를 많이 쓰는 기기", "확인할 것"],
  "rows": [["카페", "커피머신, 제빙기, 온수기", "커피머신 전용 회로, 누전"],
           ["음식점", "전기그릴, 냉장·냉동고, 식기세척기", "회로 과부하, 주방 습기 누전"],
           ["미용실", "드라이어 여러 대, 온수기", "동시 사용 시 과부하"],
           ["편의점·마트", "쇼케이스, 냉동고", "24시간 기기 회로 분리, 정전 대비"],
           ["간판·외부 조명", "LED 간판, 타이머", "외부 누전, 타이머 고장"]],
  "cap": "",
  "guide": "guide-breaker-trips"},
 "rural": {
  "title": "{n} 전원주택·농가·창고 전기, 누전이 잦은 곳 따로 있다",
  "paras": ["{n}처럼 단독주택과 전원주택, 농가 창고가 많은 지역은 아파트와 고장 양상이 다릅니다. 집과 창고, 비닐하우스, 외부 수도·조명까지 전선이 길게 나가 있어, 비바람과 습기에 노출된 구간에서 누전이 자주 생깁니다.",
            "땅에 묻힌 전선이나 외벽을 타고 나간 선이 손상되면 맑은 날엔 멀쩡하다가 비만 오면 차단기가 떨어집니다. 구간을 나눠 절연저항을 재면 어느 선이 문제인지 찾을 수 있습니다. 지하수 모터, 보일러, 전기온수기도 자주 보는 원인입니다."],
  "head": ["장소", "자주 생기는 문제", "예방·조치"],
  "rows": [["외부 조명·외부 콘센트", "빗물 유입 누전", "방수형 기구, 덮개 콘센트"],
           ["창고·비닐하우스 배선", "피복 손상, 쥐 피해", "배관 보호, 구간 교체"],
           ["지하수 모터·물탱크", "모터 누전, 압력스위치 고장", "모터 절연 측정, 부품 교체"],
           ["보일러·전기온수기", "기기 내부 누전", "기기 분리 측정"],
           ["농사용 전기(계량기 분리)", "용량 부족, 신청 절차", "한전 신청 안내, 인입 공사"]],
  "cap": "",
  "guide": "guide-leakage-check"},
 "factory": {
  "title": "{n} 공장·창고 전기, 3상 동력과 분전반 점검 포인트",
  "paras": ["{n} 일대에는 소규모 공장과 물류창고가 있어 3상 동력(모터·컴프레서·용접기 등) 전기 문의가 있습니다. 공장 전기는 동력반과 전등·전열 분전반이 나뉘어 있고, 기계를 늘리면서 배선만 덧붙인 경우가 많습니다.",
            "모터가 갑자기 멈추거나 동력 차단기가 떨어지면 과부하, 결상(3상 중 한 상이 끊김), 누전 가운데 무엇인지부터 측정합니다. 원인에 따라 차단기·전자접촉기 교체, 회로 증설, 배선 정리로 해결합니다."],
  "head": ["증상", "의심 원인", "점검"],
  "rows": [["모터가 '웅' 소리만 나고 안 돎", "결상, 접촉기 접점 불량", "상별 전압·전류 측정"],
           ["동력 차단기가 자주 떨어짐", "과부하, 모터 절연 저하", "부하 전류, 절연저항 측정"],
           ["전등·콘센트 쪽만 떨어짐", "전열 회로 과부하, 누전", "회로별 측정"],
           ["분전반 단자 변색", "접속부 발열", "단자 재체결, 부품 교체"]],
  "cap": "",
  "guide": "guide-breaker-trips"},
 "villa": {
  "title": "{n} 빌라·다세대 전기, 우리 집 문제인지 건물 문제인지 구분하기",
  "paras": ["{n}에는 빌라·다세대 주택이 많습니다. 빌라는 세대 분전반, 건물 계량기함, 계단·주차장 공용 전기가 섞여 있어, 정전이나 차단기 문제가 생겼을 때 어디를 봐야 할지 헷갈리기 쉽습니다.",
            "우리 집만 꺼졌다면 세대 분전반이나 계량기함의 세대 차단기를, 건물 전체가 꺼졌다면 건물 인입 차단기나 한전 쪽을 봐야 합니다. 오래된 빌라는 계량기함 단자 노후로 한 세대만 전기가 끊기는 경우도 있습니다."],
  "head": ["상황", "먼저 볼 곳", "연락할 곳"],
  "rows": [["우리 집만 전부 꺼짐", "세대 분전반 메인, 계량기함 세대 차단기", "전기업체"],
           ["일부 방·콘센트만 꺼짐", "세대 분전반 분기 차단기", "전기업체"],
           ["건물 전체가 꺼짐", "건물 인입 차단기, 이웃집 상황", "건물 관리인·한전(123)"],
           ["계단·주차장 등만 꺼짐", "공용 분전반", "건물 관리인·전기업체"]],
  "cap": "한전 고객센터는 국번 없이 123입니다.",
  "guide": "guide-power-out"},
 "oneroom": {
  "title": "{n} 원룸·다가구 전기, 한 세대만 자꾸 나갈 때",
  "paras": ["{n}처럼 원룸·다가구 주택이 많은 동네는 세대마다 작은 분전반이 있고, 건물 계량기함과 공용 분전반이 따로 있습니다. 한 세대에서 전열기·에어컨·전기레인지를 동시에 쓰면 세대 차단기 용량을 넘기 쉽습니다.",
            "같은 세대만 반복해서 전기가 나간다면 세대 차단기 노후, 계량기함 단자 풀림, 세대 안 가전 누전 가운데 무엇인지 측정으로 구분해야 합니다. 건물주라면 세대별로 한 번에 점검해 두는 편이 민원을 줄입니다."],
  "head": ["증상", "의심 원인", "조치"],
  "rows": [["전열기 켜면 세대 전기가 나감", "세대 차단기 용량 초과", "사용 분산, 필요 시 회로 조정"],
           ["아무것도 안 했는데 나감", "차단기 노후, 단자 풀림", "차단기 교체, 단자 재체결"],
           ["비 오는 날 나감", "창가·욕실 콘센트 습기", "방수형 교체, 절연 측정"],
           ["복도·계단 등만 꺼짐", "공용 분전반·센서", "공용 회로 점검"]],
  "cap": "",
  "guide": "guide-power-out"},
 "livestock": {
  "title": "{n} 축사·농장 전기, 멈추면 안 되는 설비 점검하기",
  "paras": ["{n}에는 축사와 농장 시설이 있어 환풍기, 보온등·히터, 급수 펌프처럼 쉬지 않고 돌아가는 설비가 많습니다. 이런 설비가 멈추면 가축 피해로 바로 이어지기 때문에 차단기 한 번 떨어지는 것도 큰일입니다.",
            "축사는 먼지와 습기, 암모니아 가스 때문에 배선과 단자가 일반 건물보다 빨리 상하고, 쥐가 전선 피복을 갉는 일도 흔합니다. 계절이 바뀔 때 절연저항과 누전차단기 동작을 점검해 두면 갑작스러운 정전을 크게 줄일 수 있습니다."],
  "head": ["설비", "자주 생기는 문제", "점검·조치"],
  "rows": [["환풍기", "모터 누전, 먼지 과열", "모터 절연 측정, 청소"],
           ["보온등·히터", "과부하, 피복 열화", "회로 분리, 내열 배선"],
           ["급수·분뇨 펌프", "습기 누전", "방수 처리, 누전차단기 점검"],
           ["분전반", "부식, 쥐 피해", "밀폐형 함체, 단자 정비"]],
  "cap": "",
  "guide": "guide-leakage-check"},
}
TOPIC_SHORT = {'panel_age': ('분전반·차단기 노후', '25년 넘은 집, 분전반·차단기 점검'), 'old_outlet': ('콘센트·스위치 노후', '헐거운 콘센트·스위치 교체'), 'fluorescent': ('형광등 → LED', '형광등·안정기 LED 교체'), 'new_circuit': ('가전 전용 회로', '인덕션·건조기 전용 회로 증설'), 'led_module': ('LED 방등 고장', 'LED 방등 모듈·컨버터 교체'), 'kitchen_leak': ('주방 콘센트 누전', '주방·아일랜드 콘센트 누전 수리'), 'shop': ('매장 차단기 과부하', '상가·매장 전기 증설·누전 수리'), 'rural': ('외부 배선 누전', '전원주택·창고 누전 수리'), 'factory': ('공장 3상 동력', '공장 3상 동력·분전반 점검'), 'villa': ('빌라 정전·차단기', '빌라·다세대 정전·차단기 수리'), 'oneroom': ('원룸 세대 정전', '원룸·다가구 정전·차단기 수리'), 'livestock': ('축사 설비 누전', '축사·농장 전기 설비 점검')}
TOPIC_ALT = {'panel_age': ['분전반 문을 열었을 때 차단기 손잡이 색이 누렇게 바랬거나, 차단기 사이 단자 쪽이 검게 그을려 있다면 {n} 집의 분전반이 오래 일했다는 표시입니다. 이런 상태에서 에어컨·인덕션을 함께 쓰면 차단기가 떨어지거나 단자에서 열이 납니다.', '교체 여부는 겉모습만으로 정하지 않습니다. 누전차단기 시험버튼 동작, 회로별 절연저항, 사용 전류를 재 본 뒤 필요한 차단기만 바꿀지 분전반 전체를 바꿀지 말씀드립니다.'], 'old_outlet': ['{n}에서 콘센트 문의를 받고 가 보면, 플러그가 빠질 듯 헐겁게 꽂히는 콘센트가 한 집에 몇 개씩 있는 경우가 많습니다. 헐거운 콘센트는 접촉 부분이 좁아져 열이 나고, 오래 쓰면 커버가 변색되고 그을음이 생깁니다.', '스위치도 마찬가지로 안쪽 접점이 닳으면 여러 번 눌러야 켜지거나 딸깍 소리만 납니다. 문제가 보이는 것부터 바꾸되, 같은 시기에 단 것이 많다면 한 번에 정리하는 쪽이 출장비를 아낍니다.'], 'fluorescent': ['형광등 끝부분이 검게 변하거나 켤 때 한참 깜빡이다 켜진다면 램프보다 안정기가 지친 경우가 많습니다. {n}처럼 오래된 단지에서 자주 보는 증상입니다.', '형광등 자리에 LED 등기구를 달면 같은 밝기에 전기를 덜 쓰고, 안정기 고장도 사라집니다. 기존 천장 배선을 그대로 쓰는 경우가 많아 공사는 등기구 교체로 끝나는 편입니다.'], 'new_circuit': ['입주하고 나서 {n} 집에 인덕션, 식기세척기, 건조기, 의류관리기를 하나씩 들이다 보면 어느 날부터 주방이나 베란다 차단기가 떨어지기 시작합니다. 차단기 고장이 아니라 한 회로에 걸리는 전기가 한계를 넘은 것입니다.', '해결 방법은 큰 가전마다 길을 따로 내 주는 것, 즉 전용 회로입니다. 분전반 빈 자리에 차단기를 추가하고 맞는 굵기의 전선으로 콘센트까지 새로 연결합니다.'], 'led_module': ['LED 등은 형광등보다 오래 간다고 알려져 있지만, {n} 단지처럼 입주한 지 몇 년 지나면 고장이 하나둘 생깁니다. 특히 전원을 바꿔 주는 컨버터가 열에 약해 먼저 고장 나는 경우가 많습니다.', '모듈이나 컨버터만 교체하면 비용이 적게 들고, 등 전체를 바꾸면 밝기와 색이 새로 맞춰집니다. 다른 방 등도 같은 시기에 달렸다면 한 번에 바꾸는 쪽을 고르시는 분이 많습니다.'], 'kitchen_leak': ['{n} 단지에서 주방 차단기가 설거지할 때나 식기세척기를 돌릴 때만 떨어진다면 싱크대 아래쪽부터 확인합니다. 하부장 안 콘센트는 배수관과 가까워 습기가 차기 쉽습니다.', '물을 쓰는 가전(정수기·음식물처리기·식기세척기)을 하나씩 뽑아 보면 원인을 집에서도 어느 정도 좁힐 수 있습니다. 다 뽑아도 떨어지면 콘센트나 배선 쪽이라 측정이 필요합니다.'], 'shop': ['{n} 매장에서 차단기가 떨어지는 시간대를 보면 원인이 보이는 경우가 많습니다. 점심·저녁 피크에 떨어지면 과부하, 비 오는 날이나 청소 후에 떨어지면 누전 쪽을 먼저 의심합니다.', '업종 변경이나 인테리어 공사 때 분전반 회로를 새로 나누면 영업 중 정전을 크게 줄일 수 있습니다. 간판과 외부 조명은 따로 회로를 두어 외부 누전이 매장 안 전기를 끊지 않게 합니다.'], 'rural': ['{n}의 단독주택이나 창고는 계량기에서 집, 집에서 창고·마당까지 전선이 길게 이어집니다. 이 중 땅에 묻히거나 외벽에 노출된 구간이 비바람에 상하면 누전이 생깁니다.', '비 오는 날에만 차단기가 떨어진다면 집 안보다 집 밖 배선을 먼저 의심하세요. 외부 콘센트·조명, 지하수 모터, 보일러처럼 물과 가까운 설비가 흔한 원인입니다.'], 'factory': ['{n} 공장에서 갑자기 기계가 서면 생산이 멈추기 때문에 원인을 빨리 찾는 것이 중요합니다. 동력 차단기가 떨어졌는지, 접촉기만 붙지 않는지, 한 상이 끊겼는지를 측정기로 바로 구분합니다.', '기계를 늘릴 때마다 배선만 덧붙여 온 공장은 분전반 안이 복잡하고 단자 발열이 생기기 쉽습니다. 정기적으로 단자를 다시 조이고 절연을 재 두면 갑작스러운 정지를 크게 줄일 수 있습니다.'], 'villa': ['{n} 빌라에서 정전이 나면 먼저 우리 집만인지, 건물 전체인지부터 보세요. 그것만 알아도 어디를 확인할지, 누구에게 연락할지가 정해집니다.', '오래된 빌라는 계량기함 안 세대 차단기와 단자가 낡아 한 집만 전기가 끊기는 경우가 있고, 공용 계단 등은 공용 분전반에 따로 묶여 있습니다. 아래 표를 참고해 확인해 보세요.']}
TOPIC_TYPE_NOTE = {"oneroom": "혼합", "livestock": "노후", "panel_age": "노후", "old_outlet": "노후", "fluorescent": "노후", "villa": "혼합", "shop": "혼합",
                   "new_circuit": "신축", "led_module": "신축", "kitchen_leak": "신축", "rural": "노후", "factory": "혼합"}

exec(open(os.path.join(BASE, "seo_visual.py"), encoding="utf-8").read())
exec(open(os.path.join(BASE, "dong_data.py"), encoding="utf-8").read())

# 기존 LOCALS와 합치기 (같은 slug는 새 데이터로 보강, 새 동네는 추가)
_by_slug = {l["slug"]: l for l in LOCALS}
for _d in DONG_DATA:
    _old = _by_slug.get(_d["slug"])
    if _old:
        _old.update({k: v for k, v in _d.items() if k not in ("match",)})
        _old["match"] = sorted(set(_old["match"]) | set(_d.get("match", [])))
    else:
        LOCALS.append(_d); _by_slug[_d["slug"]] = _d
    AREA_TYPE[_d["slug"]] = TOPIC_TYPE_NOTE.get(_d["topics"][0], "혼합")

for _l in LOCALS:
    if _l["slug"] == "yangju-hoecheon":
        _l.setdefault("topics", ["led_module", "panel_age"]); _l.setdefault("near", [])
        _l.setdefault("lead", "덕정역·덕계역·회천중앙역 일대 회천지구 아파트와 빌라의 누전·차단기 수리, 전용 회로 증설, 분전반 교체를 직접 전기출장합니다.")

REGION_LABEL = {"uijeongbu": "의정부", "yangju": "양주", "dongducheon": "동두천", "hanam": "하남", "namyangju": "남양주", "guri": "구리", "pocheon": "포천", "nowon": "노원구", "dobong": "도봉구", "gangbuk": "강북구", "seongbuk": "성북구"}
SEOUL = {"nowon", "dobong", "gangbuk", "seongbuk"}
FAR = SEOUL | {"hanam", "guri", "namyangju"}

def _variants(kn, nm):
    v = [kn]
    if nm != kn: v.append(nm)
    return v

def local_cases(lp):
    return [x for x in POSTS if any(m in (x.get("location") or "") + x["title"] for m in lp["match"])]

def nearby_cases(lp, limit=3):
    near_lps = [o for o in LOCALS if o["region"] == lp["region"] and o is not lp and o["kn"] in lp.get("near", [])]
    out = []
    for o in near_lps:
        for x in local_cases(o):
            if x not in out: out.append(x)
    if len(out) < limit:
        rn = REGION_LABEL.get(lp["region"], "")
        out += [x for x in POSTS if x["region"] == rn and x not in out]
    return out[:limit]

def _v(slug, k):
    return sum(ord(c) * (i + 1) for i, c in enumerate(slug)) % k

def topic_html(key, n, v=0):
    t = TOPICS[key]
    g = next((x for x in GUIDES if x["slug"] == t["guide"]), None)
    src = TOPIC_ALT.get(key) if (v % 2 and key in TOPIC_ALT) else t["paras"]
    paras = "".join(f"<p>{E(p.format(n=n))}</p>" for p in src)
    rows = t["rows"]
    if len(rows) >= 4:
        o = v % len(rows); rows = (rows[o:] + rows[:o])[:len(rows) - 1]
    link = f'<p><a class="link" href="{g["slug"]}.html">더 자세히: {E(g["q"])} →</a></p>' if g else ""
    return f'<h2>{E(t["title"].format(n=n))}</h2>{paras}{topic_fig(key, n)}{table_html(t["head"], rows, t.get("cap", ""))}{link}'

def inquiry_html(lp, n):
    """시공사례가 아직 없는 동네 — 문의를 부르는 안내"""
    spots = [re.sub(r"\s*\(.*?\)", "", x) for x in (lp.get("complexes", [])[:3] or lp.get("landmarks", [])[:3])]
    where = f"{', '.join(spots)} 같은 {n} 곳곳" if spots else f"{n} 곳곳"
    v = _v(lp["slug"], 12)
    intro = [f"{n} 시공사례는 아직 홈페이지에 정리 중이지만, {where}까지 출장합니다. 아래 내용을 문자로 보내 주시면 방문 전에 원인 방향과 대략적인 작업 범위를 먼저 안내해 드립니다.",
             f"{where} 어디든 전화 한 통이면 됩니다. 처음 연락하실 때 아래처럼 알려주시면 통화가 짧아지고, 필요한 자재를 챙겨 한 번에 끝낼 수 있습니다.",
             f"홈페이지에 올린 {n} 사례는 아직 없지만 {where}도 출장 지역입니다. 증상을 이렇게 정리해 보내 주시면 현장에 가기 전에 원인을 상당 부분 좁힐 수 있습니다. 비용은 현장에서 먼저 말씀드리고 동의하신 뒤에만 작업합니다."][v % 3]
    rows = [["어디인지", f"{n} ○○아파트 ○동, ○○빌라, ○○상가 등", "이동 시간·주차 안내"],
            ["무슨 증상인지", "차단기가 떨어짐 / 탄 냄새 / 한 방만 꺼짐", "원인 방향을 먼저 좁힘"],
            ["언제부터인지", "오늘 갑자기 / 비 오는 날마다 / 가전 들인 뒤로", "누전·과부하 구분"],
            ["사진 1~2장", "분전반 문 열고 찍은 사진, 문제 콘센트·등", "맞는 자재를 챙겨 한 번에 끝냄"]]
    rows = [rows[0]] + [r for i, r in enumerate(rows[1:]) if i != v % 3]
    return (f'<section class="sec"><div class="wrap post"><div class="post-body g-body">'
            f'<h2>{E(n)} 전기수리, 처음 연락하실 때 이렇게 알려주세요</h2>'
            f'<p>{E(intro)}</p>'
            f'{table_html(["알려주실 것", "예시", "도움이 되는 이유"], rows)}'
            f'<p><a class="btn btn-y" href="sms:{TEL}">{icon("chat")} {E(n)} 증상 사진 문자로 보내기</a></p>'
            f'</div></div></section>')

def choose_html(n, v=0):
    rows = [["전기공사업 등록·자격", "분전반·배선 공사는 자격 갖춘 업체가 해야 안전하고 사후 책임이 분명함"],
            ["작업 전 원인·비용 설명", "측정 없이 '다 바꿔야 한다'는 업체는 피하기"],
            ["측정 장비 사용", "누전은 절연저항계, 과부하는 전류 측정으로 원인을 확인"],
            ["같은 규격 자재", "차단기 용량을 임의로 키우면 벽 속 전선이 과열됨"],
            ["작업 기록·사후 연락", "같은 증상이 다시 생겼을 때 빠르게 원인 확인"]]
    o = v % len(rows); rows = (rows[o:] + rows[:o])[:3]
    intro = [f"{n}에서 전기업체를 처음 부르신다면 아래 세 가지는 꼭 확인해 보세요.",
             f"{n} 전기공사업체를 고를 때 가격만큼 중요한 것이 있습니다.",
             f"같은 {n} 전기수리라도 업체마다 일하는 방식이 다릅니다. 이 정도는 물어보셔도 괜찮습니다.",
             f"{n}에서 전기출장을 부르기 전에 확인하면 좋은 것들입니다."][v % 4]
    return f'<h2>{E(n)} 전기공사업체·전기업체 고를 때 확인할 것</h2><p>{E(intro)} 스마일일렉은 전기공사기술자(중급)·전기기능사가 직접 방문해 측정으로 원인을 확인한 뒤 작업합니다.</p>{table_html(["확인할 것", "이유"], rows)}'

def glance_html(lp, n, rn):
    rows = [["행정구역", (f"서울 {rn} {n}" if lp["region"] in SEOUL else f"경기도 {rn}시 {n}") + (f" (행정동: {', '.join(lp['admin'])})" if lp.get("admin") else "")]]
    rows.append(["건물 구성", " · ".join(mix_names(lp, 1))])
    if lp.get("complexes"): rows.append(["대표 아파트", ", ".join(re.sub(r"\s*\(.*?\)", "", c) for c in lp["complexes"])])
    if lp.get("landmarks"): rows.append(["주요 장소", ", ".join(lp["landmarks"])])
    rows.append(["인근 출장", ", ".join(lp.get("near", []))])
    if lp.get("jobs"): rows.append(["자주 하는 작업", lp["jobs"]])
    th = "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in rows)
    return f'<h2>{E(n)} 한눈에 보기</h2><div class="tbl-wrap"><table class="tbl"><tbody>{th}</tbody></table></div>{building_table(lp, n)}{near_map_fig(lp, n, rn)}'

def build_local(lp):
    r = next(x for x in REGIONS if x["slug"] == lp["region"]); rn = r.get("alias") or r["name"]
    n = lp["kn"]; nm = lp["name"]
    city = REGION_LABEL.get(lp["region"], rn)
    cases = local_cases(lp)
    title = f"{n} 전기수리·전기출장 | {city} {n} 전기공사업체 - {C['name']}"
    desc = lp.get("desc") or f"{city} {n} 전기수리·전기출장 스마일일렉. {n} 전기업체로 누전·차단기·콘센트·조명 수리와 전기공사까지 직접 출장합니다. {C['phone']}"
    kws = []
    for v in _variants(n, nm):
        kws += [f"{v} 전기수리", f"{v}전기수리", f"{v} 전기출장", f"{v} 전기공사", f"{v} 전기공사업체", f"{v} 전기업체"]
    kws += [f"{city} {n} 전기수리", f"{n} 누전", f"{n} 차단기", f"{n} 콘센트", f"{n} 조명 교체"] + [f"{d} 전기수리" for d in lp.get("near", [])]
    kw = ", ".join(dict.fromkeys(kws))
    faqs = list(lp.get("faqs", []))
    v = _v(lp["slug"], 12)
    reach = (f"스마일일렉은 경기 북부와 서울 동북부를 매일 다니고 있어 {city} {n}도 일정을 맞춰 방문합니다." if lp["region"] in FAR
             else f"스마일일렉은 양주 광적면에 있어 {city} {n}까지 이동이 어렵지 않습니다.")
    gen = [(f"{n} 전기업체 오늘 출장 되나요?", f"전화로 증상을 먼저 듣고 가능한 가장 빠른 시간으로 방문 일정을 잡습니다. {reach} 타는 냄새가 나면 해당 차단기를 내려 두고 기다려 주세요."),
             (f"{n}에서 콘센트 하나, 등 하나 교체도 전기출장 오시나요?", "네. 작은 작업 한 건도 출장합니다. 사진을 먼저 보내 주시면 맞는 자재를 챙겨 한 번에 끝냅니다."),
             (f"{n} 전기공사 비용은 언제 알 수 있나요?", "전화나 사진으로 대략적인 방향을 먼저 안내하고, 현장에서 원인을 확인한 뒤 작업 전에 정확한 비용을 말씀드립니다. 동의하신 뒤에만 작업합니다.")]
    faqs.append(gen[v % 3])
    for tname in mix_names(lp, 2):
        if tname in MIX_FAQ:
            q, a = MIX_FAQ[tname][v % len(MIX_FAQ[tname])]
            faqs.insert(2, (q.format(n=n), a)); break
    crumbs = [("홈", ""), (f"{r['name']} 전기수리", f"{r['slug']}.html"), (f"{n} 전기수리", f"{lp['slug']}.html")]
    tps = list(lp.get("topics", []))
    m = lp.get("mix") or (2, 1, 1, 1, 0)
    want = []
    if m[2] >= 2 and "shop" not in tps: want.append((m[2], "shop"))
    if m[1] >= 2 and not ({"villa", "oneroom"} & set(tps)): want.append((m[1], "villa"))
    for _, k in sorted(want, reverse=True)[:1]:
        tps = tps[:2] + [k] if len(tps) >= 2 else tps + [k]
    topics = "".join(topic_html(k, n, v + i) for i, k in enumerate(tps[:3]))
    if cases:
        case_sec = cases_html(cases, f"{n} 전기수리 시공사례", limit=12)
        inq = ""
    else:
        nc = nearby_cases(lp)
        case_sec = cases_html(nc, f"{n} 인근 시공사례", limit=3) if nc else ""
        inq = inquiry_html(lp, n)
    others = "".join(f'<a class="chip" href="{o["slug"]}.html">{E(o["kn"])} 전기수리</a>' for o in LOCALS if o["region"] == lp["region"] and o is not lp)
    lead = lp.get("lead") or f"{city} {n} 아파트·주택·상가의 누전·차단기 수리, 콘센트·스위치·조명 교체, 분전반 공사까지 전기공사기술자가 직접 전기출장합니다."
    intro = lp.get("intro", "")
    thumb = f"images/dong/{lp['slug']}.jpg"
    has_thumb = os.path.exists(os.path.join(BASE, "static", thumb))
    og = f"{C['domain']}/{thumb}" if has_thumb else None
    alt = f"{city} {n} 전기수리 전기출장 스마일일렉"
    thumb_html = f'<figure class="dong-thumb"><img src="{thumb}" alt="{E(alt)}" width="1200" height="630"></figure>' if has_thumb else ""
    page = head(title, desc, f"{lp['slug']}.html", kw, [business_schema([f"{city} {n}"]), faq_schema(faqs), howto_schema(f"{n} 전기수리 진행 순서", STEPS), crumbs_schema(crumbs)], og=og) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › <a href="{r['slug']}.html">{E(r['name'])}</a> › {E(n)} 전기수리</nav>
  <h1><em>{E(n)}</em> 전기수리 · 전기공사</h1>
  <p class="lead">{E(lead)}</p>
  <div class="hero-btns"><a class="btn btn-y" href="tel:{TEL}">{icon('phone')} {E(n)} 전기출장 상담 {E(C['phone'])}</a></div>
</div></section>
{summary_cards(lp, n, city)}
<section class="sec"><div class="wrap two">
  <div><h2>{E(city)} {E(n)}, 이런 동네입니다</h2><p>{E(intro)}</p>{f'<p>{E(lp["intro2"])}</p>' if lp.get("intro2") else ""}</div>
  <div>{thumb_html}<div class="box"><h3>{E(n)}·인근 전기출장 지역</h3><ul class="areas">{"".join(f'<li>{icon("pin")}{E(a)}</li>' for a in [f"{city} {n}"] + lp.get('near', []))}</ul><p class="muted small">{E(n)} 전기수리 · {E(n)} 전기출장 · {E(n)} 전기공사업체 · {E(nm)}전기수리</p></div></div>
</div></section>
<section class="sec alt"><div class="wrap post"><div class="post-body g-body">
{glance_html(lp, n, city)}
{topics}
</div></div></section>
{case_sec}
{inq}
{symptom_links_html(lp['slug'], lp['kn'])}
<section class="sec"><div class="wrap post"><div class="post-body g-body">
{choose_html(n, v)}
</div></div></section>
{faq_html(faqs, f"{n} 전기업체 자주 묻는 질문")}
<section class="sec"><div class="wrap"><h2>{E(city)} 다른 동네 전기수리</h2><div class="chips"><a class="chip" href="{r['slug']}.html">{E(r['name'])} 전체</a>{others}</div></div></section>
{cta(f"{n} 전기 문제, 지금 바로 상담하세요")}
""" + footer()
    write(f"{lp['slug']}.html", page)
