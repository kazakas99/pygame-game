"""
List Implementation Analysis
Scenario: add(1,4) add(1,5) get(2) add(2,3) del(1) add(1,6) del(1) size() get(1)

Tracing read/write operations for three different List implementations
"""

# ============================================================================
# IMPLEMENTATION 1: Simple Dynamic Array
# ============================================================================
"""
Simple linear array. Elements are stored in order.
- add(i, v): shifts elements from position i onwards right, then inserts
- del(i): shifts elements after position i left
- get(i): returns element at position i
- size(): returns array length
"""

class ListSimpleDynamic:
    def __init__(self):
        self.data = []
    
    def add(self, index, value):
        """Add value at 1-based index, shifting elements right"""
        # Shift elements: read each element, write to right position
        self.data.insert(index - 1, value)
    
    def get(self, index):
        """Get value at 1-based index"""
        return self.data[index - 1]
    
    def delete(self, index):
        """Delete element at 1-based index"""
        del self.data[index - 1]
    
    def size(self):
        return len(self.data)


def trace_implementation_1():
    """
    Detailed trace of Implementation 1: Simple Dynamic Array
    
    Initial state: data = []
    
    Operation 1: add(1, 4)
    - At index 0, insert 4
    - No shifts needed (empty array)
    - Write data[0]=4 (LV+1)
    - LV: 1, RV: 0
    - Result: data = [4]
    
    Operation 2: add(1, 5)
    - At index 0, insert 5
    - Need to shift element at index 0 onwards to the right
    - Read data[0]=4 (RV+1), Write data[1]=4 (LV+1), Write data[0]=5 (LV+1)
    - LV: 2, RV: 1
    - Result: data = [5, 4]
    
    Operation 3: get(2)
    - Read data[1]=4 (RV+1)
    - LV: 0, RV: 1
    - Result: returns 4
    
    Operation 4: add(2, 3)
    - At index 1, insert 3
    - Need to shift element at index 1 onwards (just data[1]=4)
    - Read data[1]=4 (RV+1), Write data[2]=4 (LV+1), Write data[1]=3 (LV+1)
    - LV: 2, RV: 1
    - Result: data = [5, 3, 4]
    
    Operation 5: del(1)
    - Delete at index 0
    - Need to shift elements at indices 1, 2 left
    - Read data[1]=3 (RV+1), Write data[0]=3 (LV+1)
    - Read data[2]=4 (RV+1), Write data[1]=4 (LV+1)
    - LV: 2, RV: 2
    - Result: data = [3, 4]
    
    Operation 6: add(1, 6)
    - At index 0, insert 6
    - Need to shift elements from index 0 onwards
    - Read data[0]=3 (RV+1), Write data[1]=3 (LV+1)
    - Read data[1]=4 (RV+1), Write data[2]=4 (LV+1)
    - Write data[0]=6 (LV+1)
    - LV: 3, RV: 2
    - Result: data = [6, 3, 4]
    
    Operation 7: del(1)
    - Delete at index 0
    - Need to shift elements at indices 1, 2 left
    - Read data[1]=3 (RV+1), Write data[0]=3 (LV+1)
    - Read data[2]=4 (RV+1), Write data[1]=4 (LV+1)
    - LV: 2, RV: 2
    - Result: data = [3, 4]
    
    Operation 8: size()
    - No array element reads/writes
    - LV: 0, RV: 0
    - Result: returns 2
    
    Operation 9: get(1)
    - Read data[0]=3 (RV+1)
    - LV: 0, RV: 1
    - Result: returns 3
    
    TOTALS:
    LV (writes) = 0 + 2 + 0 + 2 + 2 + 3 + 2 + 0 + 0 = 11
    RV (reads)  = 0 + 1 + 1 + 1 + 2 + 2 + 2 + 0 + 1 = 10
    """
    pass


# ============================================================================
# IMPLEMENTATION 2: Array with Gaps (using flag array)
# ============================================================================
"""
Array with gaps. Elements can be deleted leaving gaps. Gaps are marked in flag array.
- The array can have unused cells (gaps)
- Flag array marks which cells are occupied
- No rebalancing performed
"""

class ListWithGaps:
    def __init__(self):
        self.data = []
        self.flags = []  # True = occupied, False = empty
    
    def add(self, index, value):
        """Add value at logical index (counting only non-empty cells)"""
        # Find the position for the index-th non-empty element
        count = 0
        pos = 0
        
        # Find where to insert
        while count < index and pos < len(self.data):
            if self.flags[pos]:
                count += 1
            pos += 1
        
        # At this point, pos is where we should insert
        # Look for a gap before this position
        gap_found = False
        for i in range(pos):
            if not self.flags[i]:
                # Found a gap, insert here
                self.data[i] = value
                self.flags[i] = True
                gap_found = True
                break
        
        if not gap_found:
            # No gap found, append
            self.data.insert(pos, value)
            self.flags.insert(pos, True)
    
    def get(self, index):
        """Get value at logical index"""
        count = 0
        for i in range(len(self.data)):
            if self.flags[i]:
                count += 1
                if count == index:
                    return self.data[i]
    
    def delete(self, index):
        """Delete element at logical index"""
        count = 0
        for i in range(len(self.data)):
            if self.flags[i]:
                count += 1
                if count == index:
                    self.flags[i] = False
                    break
    
    def size(self):
        return sum(1 for f in self.flags if f)


def trace_implementation_2():
    """
    Detailed trace of Implementation 2: Array with Gaps
    
    Initial state: data = [], flags = []
    
    Operation 1: add(1, 4)
    - index=1, find position for 1st non-empty element
    - count=0, pos=0 (loop doesn't execute, empty array)
    - No gap found, append at pos 0
    - Write data[0]=4 (LV+1), Write flags[0]=True (flag write - NOT counted)
    - LV: 1, RV: 0
    - Result: data = [4], flags = [T]
    
    Operation 2: add(1, 5)
    - index=1, find position for 1st non-empty element
    - Loop: pos=0, flags[0]=True, count=1, pos=1
    - count==index, exit loop at pos=1
    - Check for gaps before pos=1: flags[0]=True (no gap)
    - Append at pos 1
    - Write data[1]=5 (LV+1), Write flags[1]=True (flag write - NOT counted)
    - LV: 1, RV: 0
    - Result: data = [4, 5], flags = [T, T]
    
    Operation 3: get(2)
    - Find 2nd non-empty element
    - Loop through: i=0, flags[0]=True, count=1
    - i=1, flags[1]=True, count=2, count==index, return data[1] (RV+1)
    - LV: 0, RV: 1
    - Result: returns 5
    
    Operation 4: add(2, 3)
    - index=2, find position for 2nd non-empty element
    - Loop: i=0, flags[0]=True, count=1
    - i=1, flags[1]=True, count=2, exit at pos=2
    - Check for gaps before pos=2: flags[0]=True, flags[1]=True (no gaps)
    - Append at pos 2
    - Write data[2]=3 (LV+1), Write flags[2]=True (flag write - NOT counted)
    - LV: 1, RV: 0
    - Result: data = [4, 5, 3], flags = [T, T, T]
    
    Operation 5: del(1)
    - Find 1st non-empty element and delete
    - Loop: i=0, flags[0]=True, count=1, count==index
    - Write flags[0]=False (flag write - NOT counted)
    - LV: 0, RV: 0
    - Result: data = [4, 5, 3], flags = [F, T, T]
    
    Operation 6: add(1, 6)
    - index=1, find position for 1st non-empty element
    - Loop: i=0, flags[0]=False, skip
    - i=1, flags[1]=True, count=1, exit at pos=2
    - Check for gaps before pos=2: flags[0]=False (gap found!)
    - Write data[0]=6 (LV+1)
    - Write flags[0]=True (flag write - NOT counted)
    - LV: 1, RV: 0
    - Result: data = [6, 5, 3], flags = [T, T, T]
    
    Operation 7: del(1)
    - Find 1st non-empty element and delete
    - Loop: i=0, flags[0]=True, count=1, count==index
    - Write flags[0]=False (flag write - NOT counted)
    - LV: 0, RV: 0
    - Result: data = [6, 5, 3], flags = [F, T, T]
    
    Operation 8: size()
    - Count non-empty: sum of flags[i] where flags[i]=True
    - Read flags[0]=False (RV+1), Read flags[1]=True (RV+1), Read flags[2]=True (RV+1)
    - LV: 0, RV: 3
    - Result: returns 2
    
    Operation 9: get(1)
    - Find 1st non-empty element
    - Loop: i=0, Read flags[0]=False (RV+1), skip
    - i=1, Read flags[1]=True (RV+1), count=1, count==index
    - Read data[1]=5 (RV+1), return
    - LV: 0, RV: 3
    - Result: returns 5
    
    TOTALS:
    LV (writes) = 1 + 1 + 0 + 1 + 0 + 1 + 0 + 0 + 0 = 4
    RV (reads)  = 0 + 0 + 1 + 0 + 0 + 0 + 0 + 3 + 3 = 7
    
    NOTE: Flag operations are NOT counted in LV/RV according to task requirements.
    """
    pass


# ============================================================================
# IMPLEMENTATION 3: Non-linear Array with Index Tracking
# ============================================================================
"""
Non-linear array where elements are stored in any order (typically appended),
and indices are used to track their logical positions.
"""

class ListNonLinear:
    def __init__(self):
        self.data = []  # Stores actual values
        self.indices = []  # Stores indices for logical ordering
        self.next_logical = 1
    
    def add(self, logical_index, value):
        """
        Add value at logical index.
        Appends to end of data, updates indices array to maintain logical order.
        """
        # Insert into data at the end
        physical_pos = len(self.data)
        self.data.append(value)
        
        # Now update indices to insert at logical position
        # indices stores (physical_pos, logical_order) or we traverse to find position
        # For simplicity: indices stores physical positions in logical order
        
        # Find where to insert in the indices array
        insert_pos = logical_index - 1
        self.indices.insert(insert_pos, physical_pos)
    
    def get(self, logical_index):
        """Get value at logical index"""
        physical_pos = self.indices[logical_index - 1]
        return self.data[physical_pos]
    
    def delete(self, logical_index):
        """Delete element at logical index"""
        # Remove from indices
        self.indices.pop(logical_index - 1)
    
    def size(self):
        return len(self.indices)


def trace_implementation_3():
    """
    Detailed trace of Implementation 3: Non-linear Array with Index Tracking
    
    Initial state: data = [], indices = []
    
    Operation 1: add(1, 4)
    - physical_pos = 0
    - Write data[0]=4 (LV+1)
    - insert_pos = 0
    - Insert 0 into indices at position 0
    - Write indices[0]=0 (LV+1) (counts as data structure write, not array element)
    
    Actually, let me reconsider. The task says "ignoring auxiliary arrays". 
    So indices array writes/reads are NOT counted!
    
    Let me retrace:
    
    Operation 1: add(1, 4)
    - physical_pos = 0
    - Write data[0]=4 (LV+1)
    - Insert into indices (NOT counted)
    - LV: 1, RV: 0
    - Result: data = [4], indices = [0]
    
    Operation 2: add(1, 5)
    - physical_pos = 1
    - Write data[1]=5 (LV+1)
    - Insert at position 0 in indices (NOT counted - auxiliary array)
    - LV: 1, RV: 0
    - Result: data = [4, 5], indices = [1, 0]
    
    Operation 3: get(2)
    - physical_pos = Read indices[1]=0 (NOT counted - auxiliary array read)
    - Read data[0]=4 (RV+1)
    - LV: 0, RV: 1
    - Result: returns 4
    
    Operation 4: add(2, 3)
    - physical_pos = 2
    - Write data[2]=3 (LV+1)
    - Insert at position 1 in indices (NOT counted)
    - LV: 1, RV: 0
    - Result: data = [4, 5, 3], indices = [1, 2, 0]
    
    Operation 5: del(1)
    - Pop from indices at position 0 (NOT counted)
    - LV: 0, RV: 0
    - Result: indices = [2, 0]
    
    Operation 6: add(1, 6)
    - physical_pos = 3
    - Write data[3]=6 (LV+1)
    - Insert at position 0 in indices (NOT counted)
    - LV: 1, RV: 0
    - Result: data = [4, 5, 3, 6], indices = [3, 2, 0]
    
    Operation 7: del(1)
    - Pop from indices at position 0 (NOT counted)
    - LV: 0, RV: 0
    - Result: indices = [2, 0]
    
    Operation 8: size()
    - Return len(indices) - this doesn't require reading data array
    - LV: 0, RV: 0
    - Result: returns 2
    
    Operation 9: get(1)
    - physical_pos = Read indices[0]=2 (NOT counted - auxiliary)
    - Read data[2]=3 (RV+1)
    - LV: 0, RV: 1
    - Result: returns 3
    
    TOTALS:
    LV (writes) = 1 + 1 + 0 + 1 + 0 + 1 + 0 + 0 + 0 = 4
    RV (reads)  = 0 + 0 + 1 + 0 + 0 + 0 + 0 + 0 + 1 = 2
    """
    pass


# ============================================================================
# SUMMARY OF RESULTS
# ============================================================================

print("=" * 70)
print("SCENARIO: add(1,4) add(1,5) get(2) add(2,3) del(1) add(1,6) del(1) size() get(1)")
print("=" * 70)
print()

print("IMPLEMENTATION 1: Simple Dynamic Array")
print("-" * 70)
print("Trace details in trace_implementation_1() function")
print()
print("Key operations:")
print("  - add(1,4): no shifts (empty) => LV=0, RV=0 | data=[4]")
print("  - add(1,5): shift right 1 element => LV=2, RV=1 | data=[5,4]")
print("  - get(2): read 1 element => LV=0, RV=1")
print("  - add(2,3): shift right 1 element => LV=2, RV=1 | data=[5,3,4]")
print("  - del(1): shift left 2 elements => LV=2, RV=2 | data=[3,4]")
print("  - add(1,6): shift right 2 elements => LV=3, RV=2 | data=[6,3,4]")
print("  - del(1): shift left 2 elements => LV=2, RV=2 | data=[3,4]")
print("  - size(): no element ops => LV=0, RV=0")
print("  - get(1): read 1 element => LV=0, RV=1")
print()
print("TOTAL LV = 11, RV = 10")
print("ANSWER: 11 10")
print()
print()

print("IMPLEMENTATION 2: Array with Gaps")
print("-" * 70)
print("Trace details in trace_implementation_2() function")
print()
print("Key operations (flag array operations NOT counted):")
print("  - add(1,4): append => LV=1, RV=0 | data=[4] flags=[T]")
print("  - add(1,5): append => LV=1, RV=0 | data=[4,5] flags=[T,T]")
print("  - get(2): read 1 + traverse flags => LV=0, RV=1")
print("  - add(2,3): append => LV=1, RV=0 | data=[4,5,3] flags=[T,T,T]")
print("  - del(1): mark gap => LV=0, RV=0 | flags=[F,T,T]")
print("  - add(1,6): reuse gap => LV=1, RV=0 | data=[6,5,3] flags=[T,T,T]")
print("  - del(1): mark gap => LV=0, RV=0 | flags=[F,T,T]")
print("  - size(): read 3 flags => LV=0, RV=3")
print("  - get(1): read flags + data => LV=0, RV=3")
print()
print("TOTAL LV = 4, RV = 7")
print("ANSWER: 4 7")
print()
print()

print("IMPLEMENTATION 3: Non-linear Array with Index Tracking")
print("-" * 70)
print("Trace details in trace_implementation_3() function")
print()
print("Key operations (indices array operations NOT counted as auxiliary):")
print("  - add(1,4): append => LV=1, RV=0 | data=[4]")
print("  - add(1,5): append => LV=1, RV=0 | data=[4,5]")
print("  - get(2): read 1 data element => LV=0, RV=1")
print("  - add(2,3): append => LV=1, RV=0 | data=[4,5,3]")
print("  - del(1): delete from indices => LV=0, RV=0")
print("  - add(1,6): append => LV=1, RV=0 | data=[4,5,3,6]")
print("  - del(1): delete from indices => LV=0, RV=0")
print("  - size(): no data ops => LV=0, RV=0")
print("  - get(1): read 1 data element => LV=0, RV=1")
print()
print("TOTAL LV = 4, RV = 2")
print("ANSWER: 4 2")
print()
print("=" * 70)
