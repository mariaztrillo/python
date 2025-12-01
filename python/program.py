# metodo de burbuia
def bubble_sort(arr):
    n= len
    for i in range(n):
        for j in range (0, n-1-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# ejemplo de uso
lista = [64, 34, 25, 12, 22, 11, 90]
print("Lista original:", lista)
sorted_lista = bubble_sort (lista)
print("Lista ordenada:", sorted_lista) 