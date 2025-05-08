import matplotlib.pyplot as plt
import csv

# FIFO Algorithm
def fifo(pages, frame_size):
    memory, queue = [], []
    page_faults = 0
    for page in pages:
        if page not in memory:
            page_faults += 1
            if len(memory) < frame_size:
                memory.append(page)
                queue.append(page)
            else:
                removed = queue.pop(0)
                memory.remove(removed)
                memory.append(page)
                queue.append(page)
    return page_faults

# LRU Algorithm
def lru(pages, frame_size):
    memory, recent = [], {}
    page_faults = 0
    for i, page in enumerate(pages):
        if page not in memory:
            page_faults += 1
            if len(memory) < frame_size:
                memory.append(page)
            else:
                in_memory_recent = {p: recent[p] for p in memory}
                lru_page = min(in_memory_recent, key=in_memory_recent.get)
                memory.remove(lru_page)
                memory.append(page)
        recent[page] = i
    return page_faults

# Optimal Algorithm
def optimal(pages, frame_size):
    memory = []
    page_faults = 0
    for i in range(len(pages)):
        page = pages[i]
        if page not in memory:
            page_faults += 1
            if len(memory) < frame_size:
                memory.append(page)
            else:
                future_indices = {
                    p: (pages[i+1:].index(p) if p in pages[i+1:] else float('inf')) for p in memory
                }
                to_remove = max(future_indices, key=future_indices.get)
                memory.remove(to_remove)
                memory.append(page)
    return page_faults

# Read page references from CSV file
def read_pages_from_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                return [int(x.strip()) for x in row]
    except Exception as e:
        print("Error reading CSV:", e)
        return []

# Get input from user or file
def get_input():
    choice = input("Enter '1' to input manually, '2' to read from CSV file: ")
    if choice == '1':
        pages = list(map(int, input("Enter the page reference string (space separated): ").split()))
        frame_size = int(input("Enter the frame size: "))
    elif choice == '2':
        file_path = input("Enter the path to the CSV file: ")
        pages = read_pages_from_csv(file_path)
        if not pages:
            print("Failed to load pages from file.")
            return [], 0
        print("Page reference string loaded:", pages)
        frame_size = int(input("Enter the frame size: "))
    else:
        print("Invalid choice.")
        return [], 0
    return pages, frame_size

# Main function
def main():
    pages, frame_size = get_input()
    if pages and frame_size > 0:
        fifo_faults = fifo(pages, frame_size)
        lru_faults = lru(pages, frame_size)
        optimal_faults = optimal(pages, frame_size)

        print("\n--- Page Fault Summary ---")
        print("FIFO Page Faults:", fifo_faults)
        print("LRU Page Faults:", lru_faults)
        print("Optimal Page Faults:", optimal_faults)

        # Plotting results with smaller output size
        algorithms = ['FIFO', 'LRU', 'Optimal']
        faults = [fifo_faults, lru_faults, optimal_faults]

        plt.figure(figsize=(6, 4))  # Smaller size
        bars = plt.bar(algorithms, faults, color=['blue', 'green', 'orange'])

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, int(yval),
                     ha='center', fontsize=10)

        plt.title('Page Faults Comparison', fontsize=12)
        plt.xlabel('Page Replacement Algorithms', fontsize=10)
        plt.ylabel('Number of Page Faults', fontsize=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.ylim(0, max(faults) + 3)
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
