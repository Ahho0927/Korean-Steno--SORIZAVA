from pynput.keyboard import Key
from hgtk.letter import compose
from hgtk.checker import has_batchim
from tqdm import tqdm

class Translation:
    def __init__(self) -> None:
        self.KEY_CHO: str = '12345qwertasdfg'
        self.KEY_JUNG: str = 'cvbnm,'
        self.KEY_JONG: str = "7890-uiop[jkl;'"
        self.KEY_NUM: list[Key] = [Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6, Key.f7, Key.f8, Key.f9, Key.f10]
        self.HANGUL_CHO = 'ㅊㅌㅋㅂㅍㅅㄷㅈㄱㅁㄹㄴㅎ'
        self.HANGUL_JUNG = 'ㅏㅓㅗㅜㅡㅣㅢ'
        self.HANGUL_JONG = 'ㄲㅎㅌㅊㅍㄱㄴㄹㅅㅂㅆㅇㅁㄷㅈㅋ'

        self.KEY_USED: str = self.KEY_CHO + self.KEY_JONG + self.KEY_JUNG
        self.KEY_TO_HANGUL: dict[str] = dict(zip(self.KEY_USED, 'ㅊㅌㅋㅂㅍㅅㄷㅈㄱ㈊ㅁㄹㄴㅎㅢㄲㅎㅌㅊㅍㄱㄴㄹㅅㅂㅆㅇㅁㄷㅈㅗㅏㅜㅡㅓㅣ'))
        self.KEY_TO_NUM: dict[Key, str] = {Key.f1: '1', Key.f2: '2', Key.f3: '3', Key.f4: '4', Key.f5: '5', Key.f6: '6', Key.f7: '7', Key.f8: '8', Key.f9: '9', Key.f10: '0'}
        self.HANGUL_COMBINE_CHO: dict[str] = {'ㄱ': 'ㄱ', 'ㄱㅎ': 'ㄲ', 'ㄴ': 'ㄴ', 'ㄷ': 'ㄷ', 'ㄷㄹ': 'ㄸ', 'ㄹ': 'ㄹ', 'ㅁ': 'ㅁ', 'ㅂ': 'ㅂ', 'ㄱㅂ': 'ㅃ', 'ㅅ': 'ㅅ', 'ㅁㅅ': 'ㅆ', 'ㅇ': 'ㅇ', 'ㅈ': 'ㅈ', 'ㄴㅈ': 'ㅉ', 'ㅊ': 'ㅊ', 'ㅋ': 'ㅋ', 'ㅌ': 'ㅌ', 'ㅍ': 'ㅍ', 'ㅎ': 'ㅎ'}
        self.HANGUL_COMBINE_JUNG: dict[str] = {'ㅏ': 'ㅏ', 'ㅏㅣ': 'ㅐ', 'ㅏㅡ': 'ㅑ', 'ㅏㅓ': 'ㅒ', 'ㅓ': 'ㅓ', 'ㅓㅣ': 'ㅔ', 'ㅓㅡ': 'ㅕ', 'ㅏㅓㅣ': 'ㅖ', 'ㅗ': 'ㅗ', 'ㅏㅗ': 'ㅘ', 'ㅏㅗㅣ': 'ㅙ', 'ㅗㅣ': 'ㅚ', 'ㅗㅡ': 'ㅛ', 'ㅜ': 'ㅜ', 'ㅓㅜ': 'ㅝ', 'ㅓㅜㅣ': 'ㅞ', 'ㅜㅣ': 'ㅟ', 'ㅜㅡ': 'ㅠ', 'ㅡ': 'ㅡ', 'ㅢ': 'ㅢ', 'ㅣ': 'ㅣ'}
        self.HANGUL_COMBINE_JONG: dict[str] = {'ㄱ': 'ㄱ', 'ㄲ': 'ㄲ', 'ㄱㅅ': 'ㄳ', 'ㄴ': 'ㄴ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄷ': 'ㄷ', 'ㄹ': 'ㄹ', 'ㄱㄹ': 'ㄺ', 'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ', 'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅁ': 'ㅁ', 'ㅂ': 'ㅂ', 'ㅂㅅ': 'ㅄ', 'ㅅ': 'ㅅ', 'ㅆ': 'ㅆ', 'ㅇ': 'ㅇ', 'ㅈ': 'ㅈ', 'ㅊ': 'ㅊ', 'ㅋ': 'ㅋ', 'ㅌ': 'ㅌ', 'ㅍ': 'ㅍ', 'ㅎ': 'ㅎ'}

        self.previous_result = '가'
        self.stick = False

        # Load Macros from txt file
        self.macros: dict[str] = dict()
        with open('./macros_data.txt','r', encoding='utf-16-le') as data_file:
            macros_data = data_file.readlines()

        print("Loading Macros Data ...")
        for line in tqdm(macros_data):
            if ';' in line:
                continue

            line = line.replace('\n', '').replace('#', ' ')
            key, value = line.split('\t\t')
            cho, jung, jong, num = '', '', '', ''

            if '-' in key:
                jung = '-'
                cho, jong = key.split('-')
            else:
                cho_finished = False
                for letter in key:
                    if not cho_finished:
                        if letter in self.HANGUL_CHO:
                            cho += letter
                            continue
                        if letter in self.HANGUL_JUNG:
                            cho_finished = True
                            jung += letter
                            continue
                    if letter in self.HANGUL_JUNG:
                        jung += letter
                        continue
                    if letter in self.HANGUL_JONG:
                        jong += letter
                        continue
                    num += letter

            cho, jung, jong, num = ''.join(sorted(cho)), ''.join(sorted(jung)), ''.join(sorted(jong)), ''.join(sorted(num))

            self.macros[cho+jung+jong+num] = value
        print("Done!")
        # print(self.macros)

    def get_result(self, pressed_key) -> None:
        cho, jung, jong, num = self.key_to_hangul(pressed_key)
        indicator: str = cho + jung + jong + num
        print(indicator)

        result = self.macros.get(indicator, None)
        if result:
            if '↙' in result:
                result = result.replace('↙', '')
                if self.previous_result[-1] == ' ':
                    self.stick = True
                    try:
                        self.previous_result = self.previous_result[:-1]
                    except:
                        self.previous_result = '가'

            if '/' in result: # Allomorphic
                results = result.split('/')
                try:
                    result = results[1]
                    if has_batchim(self.previous_result[-1]):
                        result = results[0]
                except AttributeError:
                    result = results[0]

                

            return result
        
        try:
            if cho == '':
                cho = 'ㅇ'
            result = compose(self.HANGUL_COMBINE_CHO.get(cho, None), 
                                self.HANGUL_COMBINE_JUNG.get(jung, None), 
                                self.HANGUL_COMBINE_JONG.get(jong, None))
            
        except Exception:
            pass
            
        return result

    def key_to_hangul(self, keys: list[str]):
        cho, jung, jong, num = '', '', '', ''
        for key in keys:
            if key in self.KEY_NUM:
                num += self.KEY_TO_NUM.get(key, '')
                continue
            if key in self.KEY_CHO:
                cho += self.KEY_TO_HANGUL.get(key, '')
                continue
            if key in self.KEY_JUNG:
                jung += self.KEY_TO_HANGUL.get(key, '')
                continue
            if key in self.KEY_JONG:
                jong += self.KEY_TO_HANGUL.get(key, '')
        
        if '㈊' in cho:
            cho = cho.replace('㈊', '')
            jong += 'ㅋ'
        if 'ㅢ' in cho:
            cho = cho.replace('ㅢ', '')
            jung += 'ㅢ'
        if jung == '' and jong != '':
            print('jung -')
            jung = '-'

        return ''.join(sorted(cho)), ''.join(sorted(jung)), ''.join(sorted(jong)), ''.join(sorted(num))