#TwoSum

def twoSum(nums, target):
    left = 0
    right = len(nums) - 1
    while left < right:
        sum = nums[left] + nums[right]
        if sum == target:
            return [left, right]
        elif sum < target:
            left += 1
        else:
            right -= 1

#example
target = 25
ms1 = [3,8,9,11,16,18,19,21]
result = twoSum(ms1, target)
print('twoSum:', result)


# reverseArray

def reverseArray(arr):
    left = 0
    right = len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

ms2 = [3,8,6,9,9,8,6]
print('no reversed:', ms2)
print('reversed:', reverseArray(ms2))

#partically reversed

def partiallyReverseArray(arr, left, right):
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left+=1
        right-=1

def solution(arr, k):
    n= len(arr)
    k = k % n
    partiallyReverseArray(arr, 0, n - 1)
    partiallyReverseArray(arr, 0, k - 1)
    partiallyReverseArray(arr, k, n - 1)
    return arr

ms3 = [1, 2, 3, 4, 5, 6, 7]
print('no reversed:', ms3)
k = 3
print('partially reversed:', solution(ms3, k))

#merge 2 sorted arrays

def mergeSortedArrays(arr1, arr2):
    merged_array = []
    i,j=0,0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1
    # Append any remaining elements from either array
    merged_array.extend(arr1[i:])
    merged_array.extend(arr2[j:])
    return merged_array

ms4 =[3,8,10,11]
ms5 =[1,7,9]
print('merged sorted arrays:', mergeSortedArrays(ms4, ms5))

#merge 2 sorted arrays without extra space

def mergeSortedArraysInPlace(arr1, arr2):
    pointer1 = len(arr1)-len(arr2) - 1
    pointer2 = len(arr2) - 1
    pointer3 = len(arr1) - 1
    while pointer2>=0:
        if pointer1 >= 0 and arr1[pointer1] > arr2[pointer2]:
            arr1[pointer3] = arr1[pointer1]
            pointer1 -= 1
        else:
            arr1[pointer3] = arr2[pointer2]
            pointer2 -= 1
        pointer3 -= 1
    return arr1

ms6 = [3,8,10,11,0,0,0]
ms7 = [1,7,9]
print('merged sorted arrays in place:', mergeSortedArraysInPlace(ms6, ms7))

#minimal size of subarray with sum greater than or equal to target

def minSubArrayLen(target, nums):
    minlen=float('inf')
    left=0
    sum=0
    for right in range(len(nums)):
        sum+=nums[right]
        while sum>=target:
            window_size=right-left+1
            if window_size<minlen:
                    minlen=window_size
            sum-=nums[left]
            left+=1
    return 0 if minlen==float('inf') else minlen

target=7
ms8=[2,3,1,2,4,3]
print('minimal size of subarray with sum greater than or equal to target:', minSubArrayLen(target, ms8))

#0/1 sort

def sort_binary_array(arr):
    left = 0
    right = len(arr) - 1
    while left < right:
        if arr[left] == 0:
            left += 1
        elif arr[right] == 1:
            right -= 1
        else:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1
    return arr

ms9 = [0, 1, 1, 0, 1, 0, 1, 0]
print('sorted binary array:', sort_binary_array(ms9))

#Netherlands flag problem

def sort_colors(arr):
    low = 0
    mid = 0
    high = len(arr) - 1
    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
    return arr

ms10 = [2, 0, 2, 1, 1, 0]
print('sorted colors:', sort_colors(ms10))

#even forward

def even_first(arr):
    evenIndex = 0
    for i in range(len(arr)):
        if arr[i] % 2 == 0:
            arr[evenIndex], arr[i] = arr[i], arr[evenIndex]
            evenIndex += 1
    return arr

ms11 = [7,3,2,4,1,11,8,9]
print('even first:', even_first(ms11))

#zero last

def zero_last(arr):
    zeroIndex=len(arr)-1
    for i in range(len(arr)-1, -1, -1):
        if arr[i]==0:
            arr[zeroIndex], arr[i] = arr[i], arr[zeroIndex]
            zeroIndex-=1
    return arr

ms12 = [0, 0, 1, 0, 3, 12]
print('zero last:', zero_last(ms12))
ms13=[0, 33, 57, 88, 60, 0, 0, 80, 99]
print('zero last:', zero_last(ms13))
ms14= [0, 0, 0, 18, 16, 0, 0, 77, 99]
print('zero last:', zero_last(ms14))
