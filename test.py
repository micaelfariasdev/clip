def wordBreak(self, s: str, wordDict: list[str]) -> bool:
            
        def construct(current,wordDict, memo={}):
            if current in memo:
                return memo[current]

            if not current:
                return True

            for word in wordDict:
                if current.startswith(word):
                    new_current = current[len(word):]
                    if construct(new_current,wordDict,memo):
                        memo[current] = True
                        print(memo)
                        return True
            memo[current] = False
            print(memo)
            return False

        return construct(s,wordDict)

wordBreak(0, "aaaaaa",["aa","a"])
wordBreak(0, "leetcode",["leet","code"])
wordBreak(0, "applepenapple",["apple","pen"])
wordBreak(0, "cars",["car","ca","rs"])