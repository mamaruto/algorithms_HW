from collections import defaultdict

'''
1. Целая часть квадратного корня

Нужно найти наибольшее m, для которого m*m <= n.
При n >= 2 корень не больше n // 2, так что ищем на отрезке [1, n // 2].
m*m растёт вместе с m. Если mid*mid <= n, ответ равен mid или лежит
правее, иначе он левее. За шаг отрезок сокращается вдвое,
шагов выходит около log2(n), отсюда O(log n).
'''
def my_sqrt(n):
    if n < 0:
        raise ValueError("number must be non-negative")
    if n < 2:
        return n

    left, right = 1, n // 2
    ans = 1
    while left <= right:
        mid = (left + right) // 2
        if mid * mid <= n:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1
    return ans


'''
2. Два ксерокса

Пока нет ни одной копии, второму ксероксу не с чего копировать.
Первую копию делаем на быстром за min(x, y) минут, потом оба
работают параллельно над оставшимися N-1.

За время t первый успеет t // x копий, второй t // y. Если в сумме
это >= N-1, времени хватает. С ростом t копий не становится меньше,
поэтому подходит бинпоиск. Сверху время ограничено (N-1) * min(x, y):
столько уйдёт, если быстрый ксерокс будет работать один.
'''
def copy_time(n, x, y):
    if n == 1:
        return min(x, y)

    def enough(t):
        return t // x + t // y >= n - 1

    left, right = 0, (n - 1) * min(x, y)
    while left < right:
        mid = (left + right) // 2
        if enough(mid):
            right = mid
        else:
            left = mid + 1
    return left + min(x, y)


'''
3. Накормить животных

Сортируем животных по аппетиту и порции по размеру. Идём по порциям
от меньшей к большей. Если порции хватает самому неприхотливому из
ненакормленных, отдаём её ему. Если не хватает, она не подойдёт и
остальным (они едят больше), и её можно пропустить.

Почему так получается максимум: допустим, в каком-то лучшем
распределении животное получило порцию больше, чем ему нужно,
а маленькая подходящая ушла кому-то ещё или осталась лишней.
Если поменять их местами, все накормленные останутся накормленными.
Значит, раздавать минимально достаточные порции не хуже.
Время O(n log n + m log m), почти всё уходит на сортировку.
'''
def feed_animals(animals, food):
    animals = sorted(animals)
    food = sorted(food)

    count = 0
    i = 0
    for portion in food:
        if i == len(animals):
            break
        if portion >= animals[i]:
            count += 1
            i += 1
    return count


'''
4. Найти лишнюю букву

У XOR есть свойства x ^ x = 0 и x ^ 0 = x, а порядок операндов
не важен. Ксорим коды всех символов из a и b: каждая общая буква
попадётся чётное число раз и обнулится, останется код лишней.
O(n) по времени, O(1) по памяти.
'''
def find_extra_letter(a, b):
    res = 0
    for ch in a:
        res ^= ord(ch)
    for ch in b:
        res ^= ord(ch)
    return chr(res)


'''
Второй вариант через подсчёт: тоже O(n), но со словарём.
Буквы из b прибавляем, буквы из a вычитаем. Та, у которой
счётчик остался равен 1, и есть добавленная.
'''
def find_extra_letter_count(a, b):
    cnt = defaultdict(int)
    for ch in b:
        cnt[ch] += 1
    for ch in a:
        cnt[ch] -= 1
    for ch, c in cnt.items():
        if c == 1:
            return ch
    return ""


'''
5. Сумма двух элементов

Проходим по массиву один раз и складываем просмотренные числа
в словарь. Для текущего num ищем в нём target - num: если нашлось,
пара готова. Поиск в словаре в среднем O(1), так что вместо двух
вложенных циклов хватает одного прохода, O(n).
num кладём в словарь после проверки, иначе при target = 2*num
число сложилось бы само с собой.
'''
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        need = target - num
        if need in seen:
            return [need, num]
        seen[num] = i
    return []


'''
6. Группировка анаграмм

Анаграммы состоят из одних и тех же букв, значит им можно дать
общий ключ и разложить слова по словарю ключ -> список.
Ключом могло бы быть отсортированное слово, но сортировка стоит
O(k log k). Я считаю, сколько раз встречается каждая из 26 букв,
и беру этот кортеж: O(k) на слово, всего O(n * k).
Для букв не из a-z счётчики не подойдут, там проще sorted(word).
'''
def group_anagrams(strs):
    groups = defaultdict(list)
    for word in strs:
        counts = [0] * 26
        for ch in word:
            counts[ord(ch) - ord('a')] += 1
        groups[tuple(counts)].append(word)
    return list(groups.values())


if __name__ == "__main__":
    print("1. корень")
    for n in [0, 1, 2, 4, 8, 15, 16, 17, 99, 100, 10**12]:
        print(f"  sqrt({n}) = {my_sqrt(n)}")

    print("2. ксероксы")
    print("  N=4, x=1, y=1 ->", copy_time(4, 1, 1))   # 3
    print("  N=5, x=1, y=2 ->", copy_time(5, 1, 2))   # 4
    print("  N=1, x=3, y=5 ->", copy_time(1, 3, 5))   # 3

    print("3. животные")
    print("  ", feed_animals([3, 4, 7], [8, 1, 2]))          # 1
    print("  ", feed_animals([3, 8, 1, 4], [1, 1, 2]))       # 1
    print("  ", feed_animals([1, 2, 2], [1, 2, 3, 4]))       # 3

    print("4. лишняя буква")
    print("  ", find_extra_letter("abcd", "abcde"))          # e
    print("  ", find_extra_letter("", "y"))                  # y
    print("  ", find_extra_letter_count("aabb", "babza"))    # z

    print("5. two sum")
    print("  ", two_sum([2, 7, 11, 15], 9))     # [2, 7]
    print("  ", two_sum([3, 2, 4], 6))          # [2, 4]
    print("  ", two_sum([3, 3], 6))             # [3, 3]
    print("  ", two_sum([1, 2, 3], 100))        # []

    print("6. анаграммы")
    print("  ", group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
