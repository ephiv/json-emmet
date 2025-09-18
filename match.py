# https://stackoverflow.com/questions/9683745/how-to-replace-all-instances-of-a-sub-sequence-in-a-list-in-python
def match(pattern, list):
    matches = []
    m = len(list)
    n = len(pattern)

    rightMostIndexes = preprocessForBadCharacterShift(pattern)

    alignedAt = 0
    while alignedAt + (n - 1) < m:

        for indexInPattern in range(n-1, -1, -1):
            indexInlist = alignedAt + indexInPattern
            x = list[indexInlist]
            y = pattern[indexInPattern]

            if indexInlist >= m:
                break

            if x != y:

                r = rightMostIndexes.get(x)

                if x not in rightMostIndexes:
                    alignedAt = indexInlist + 1

                else:
                    shift = indexInlist - (alignedAt + r)
                    alignedAt += (shift > 0 and shift or alignedAt + 1)

                break
            elif indexInPattern == 0:
                matches.append(alignedAt)
                alignedAt += 1


    return matches

def preprocessForBadCharacterShift(pattern):
    map = { }
    for i in range(len(pattern)-1, -1, -1):
        c = pattern[i]
        if c not in map:
            map[c] = i

    return map