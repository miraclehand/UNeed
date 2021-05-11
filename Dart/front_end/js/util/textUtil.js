const F = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
           'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
           'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
const S = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ',
           'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ',
           'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'];
const T = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ',
           'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
           'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ',
           'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];

export function getDisassembled(value) {
    let i, c, uni
    let fn, sn, tn, fst

    fst = ''
    for (i = 0; c = value.charCodeAt(i) ; ++i ) {
        if (c < 44032 || c > 55203) {
            fst += value.charAt(i)
            continue; 
        }

        uni = c - 44032

        tn = uni % 28; // 종성 
        sn = ((uni - tn) / 28 ) % 21; // 중성 
        fn = (((uni - tn) / 28 ) - sn ) / 21; // 초성 

        fst += F[fn] + S[sn] + T[tn]
    }
    return fst
}

export function findText(text1, text2) {
    return text1.indexOf(getDisassembled(text2.toUpperCase()))
}

function checkBatchimEnding(word) {
    if (typeof word !== 'string') return null;
   
    var lastLetter = word[word.length - 1];
    var uni = lastLetter.charCodeAt(0);
        
    if (uni < 44032 || uni > 55203) return null;
           
    return (uni - 44032) % 28 != 0;
}

