import tkinter as tk
from tkinter import ttk, messagebox
import random, time
import math

# ----------------------- GLOBALS -----------------------
data, queue_items, stack_items = [], [], []
STACK_CAP, QUEUE_CAP, CQ_CAP = 7, 20, 10
cq, cq_front, cq_rear = [None]*CQ_CAP, -1, -1

# ----------------------- UTILS -----------------------
def pause():
    time.sleep(speed_scale.get())

def get_color_array(lst, highlight=[]):
    base_color = color_var.get()
    return ['orange' if i in highlight else base_color for i in range(len(lst))]

# ----------------------- DRAW -----------------------
def draw_data(lst, mode='horizontal', highlight=[]):
    canvas.delete("all")
    if mode=='stack': draw_stack(lst); return
    if mode=='queue': draw_queue(lst); return
    if mode=='cqueue': draw_cqueue(lst); return
    if not lst: return

    # Draw bars for sorting
    c_w, c_h = 700, 300
    bar_w = c_w / (len(lst)+1)
    max_val = max([x for x in lst if x is not None] or [1])
    colors = get_color_array(lst, highlight)
    for i, val in enumerate(lst):
        h = (val/max_val*280) if val is not None else 0
        x0, y0, x1, y1 = i*bar_w+5, c_h-h, (i+1)*bar_w, c_h
        canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline='black')
        canvas.create_text(x0+5, y0, anchor=tk.SW, text=str(val))
    root.update_idletasks()

def draw_stack(stack):
    canvas.delete("all")
    if not stack: return
    c_w, c_h = 700, 300
    bw, bh = 200, min(60,(c_h-40)//max(1,len(stack)))
    x0, x1 = c_w/2 - bw/2, c_w/2 + bw/2
    bottom = c_h-20
    for idx, val in enumerate(stack):
        top = bottom-bh
        col = 'orange' if idx==len(stack)-1 else 'lightblue'
        canvas.create_rectangle(x0, top, x1, bottom, fill=col, outline='black')
        canvas.create_text((x0+x1)/2, (top+bottom)/2, text=str(val))
        bottom = top-5
    canvas.create_line(x0-10, c_h-15, x1+10, c_h-15, width=2)
    canvas.create_text((x0+x1)/2, c_h-5, text=f"STACK (top ↑) Capacity: {STACK_CAP}")
    root.update_idletasks()

def draw_queue(q):
    canvas.delete("all")
    display = [str(x) for x in q]
    canvas.create_text(10, 50, anchor='nw', text='  '.join(display), font=('Arial', 20))
    root.update_idletasks()

def draw_cqueue(q):
    canvas.delete("all")
    c_w, c_h = 350, 350
    radius = 120
    center_x, center_y = c_w/2, c_h/2
    for i, val in enumerate(q):
        if val is None: continue
        angle = 2*math.pi*i/CQ_CAP
        x = center_x + radius*math.cos(angle)
        y = center_y + radius*math.sin(angle)
        canvas.create_oval(x-20, y-20, x+20, y+20, fill='lightblue', outline='black')
        canvas.create_text(x, y, text=str(val))
    # Show front and rear
    if cq_front != -1:
        f_angle = 2*math.pi*cq_front/CQ_CAP
        r_angle = 2*math.pi*cq_rear/CQ_CAP
        fx = center_x + radius*math.cos(f_angle)
        fy = center_y + radius*math.sin(f_angle)
        rx = center_x + radius*math.cos(r_angle)
        ry = center_y + radius*math.sin(r_angle)
        canvas.create_text(fx, fy-30, text='Front', fill='red')
        canvas.create_text(rx, ry+30, text='Rear', fill='green')
    root.update_idletasks()

# ----------------------- SORTING -----------------------
def bubble_sort():
    n=len(data)
    for i in range(n):
        for j in range(n-i-1):
            draw_data(data, highlight=[j,j+1])
            pause()
            if data[j]>data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                draw_data(data, highlight=[j,j+1])
                pause()
    draw_data(data)

def insertion_sort():
    n=len(data)
    for i in range(1,n):
        key=data[i]; j=i-1
        draw_data(data, highlight=[i]); pause()
        while j>=0 and key<data[j]:
            data[j+1]=data[j]; j-=1
            draw_data(data, highlight=[j+1]); pause()
        data[j+1]=key; draw_data(data, highlight=[j+1]); pause()
    draw_data(data)

def selection_sort():
    n=len(data)
    for i in range(n):
        min_idx=i
        for j in range(i+1,n):
            draw_data(data, highlight=[j,min_idx]); pause()
            if data[j]<data[min_idx]:
                min_idx=j
                draw_data(data, highlight=[min_idx]); pause()
        if min_idx!=i:
            data[i], data[min_idx]=data[min_idx], data[i]
            draw_data(data, highlight=[i,min_idx]); pause()
    draw_data(data)

def merge_sort(lst=None,l=0,r=None):
    if lst is None: lst=data; r=len(lst)-1
    if l<r:
        m=(l+r)//2
        merge_sort(lst,l,m)
        merge_sort(lst,m+1,r)
        merge(lst,l,m,r)
        draw_data(lst, highlight=list(range(l,r+1))); pause()

def merge(lst,l,m,r):
    L,R,lst_idx=lst[l:m+1],lst[m+1:r+1],l
    i=j=0
    while i<len(L) and j<len(R):
        if L[i]<=R[j]: lst[lst_idx]=L[i]; i+=1
        else: lst[lst_idx]=R[j]; j+=1
        lst_idx+=1
    while i<len(L): lst[lst_idx]=L[i]; i+=1; lst_idx+=1
    while j<len(R): lst[lst_idx]=R[j]; j+=1; lst_idx+=1

# ----------------------- QUEUE -----------------------
def enqueue(val=None):
    global queue_items
    if len(queue_items) >= QUEUE_CAP:
        funny_msgs = [
            "Whoa! Queue is stuffed like a burrito 🌯",
            "Queue says: 'Nope, I'm full! Go take a nap 😴'",
            "Queue is more crowded than a concert 🎤🎶",
            "Queue overflow! Someone call Tetris 🟦🟩🟨",
            "Queue says: 'I can't even... 😵‍💫'"
        ]
        messagebox.showwarning("Queue Full", random.choice(funny_msgs))
        return
    queue_items.append(val if val is not None else random.randint(1,50))
    draw_data(queue_items, mode='queue')

def dequeue():
    global queue_items
    if queue_items:
        queue_items.pop(0)
        draw_data(queue_items, mode='queue')
        if not queue_items:
            messagebox.showinfo("Queue Empty", random.choice([
                "Oops! Queue vanished like magic ✨",
                "Queue is now empty! Ghosts did it 👻",
                "All gone! Queue went on vacation 🏖",
                "Queue is emptier than my coffee cup ☕",
                "Nothing to dequeue! Queue is ghosting you 👀"
            ]))
    else:
        messagebox.showinfo("Queue Empty", random.choice([
            "Queue is emptier than my fridge 🥲",
            "Queue is empty, nothing to dequeue 😅",
            "Queue is chilling empty, take a break 💤"
        ]))

# ----------------------- STACK -----------------------
def push(val=None):
    global stack_items
    if len(stack_items) >= STACK_CAP:
        messagebox.showwarning("Stack Full", random.choice([
            "Stack says: 'I can't take it anymore! 🤯'",
            "Stack is bursting! Somebody help 🧱",
            "Stack overflow! Alert the firefighters 🚒🔥",
            "Stack is full! Time for a stack party 🎉",
            "Stack groans: 'Too many items, send snacks 🍕'"
        ]))
        return
    stack_items.append(val if val is not None else random.randint(1,50))
    draw_data(stack_items, mode='stack')

def pop():
    global stack_items
    if stack_items:
        stack_items.pop()
        draw_data(stack_items, mode='stack')
    else:
        messagebox.showinfo("Stack Empty", random.choice([
            "Stack is empty... nothing to pop 😅",
            "Stack cries: 'Help! I’m empty!' 😭",
            "No items left! Stack is on a diet 🥗",
            "Pop failed! Stack is chilling 🧊",
            "Stack yawns: 'I need more stuff 💤'"
        ]))

# ----------------------- CIRCULAR QUEUE -----------------------
def circular_enqueue(val=None):
    global cq, cq_front, cq_rear
    if (cq_front==0 and cq_rear==CQ_CAP-1) or (cq_rear+1)%CQ_CAP==cq_front:
        messagebox.showwarning("Circular Queue Full", random.choice([
            "Circular Queue is full! Can't spin anymore 🔄",
            "No room left! Circular Queue is dizzy 🤪",
            "Queue is circularly stuffed! 🍩",
            "Circular Queue says: 'Stop, I’m spinning out!' 🌀",
            "Overflow alert! Circular Queue is on tilt ⚠"
        ]))
        return
    v = val if val is not None else random.randint(1,50)
    if cq_front==-1: 
        cq_front=cq_rear=0
        cq[cq_rear]=v
    else: 
        cq_rear=(cq_rear+1)%CQ_CAP
        cq[cq_rear]=v
    draw_data(cq, mode='cqueue')

def circular_dequeue():
    global cq, cq_front, cq_rear
    if cq_front==-1:
        messagebox.showinfo("Circular Queue", random.choice([
            "Circular Queue is empty! Feels lonely 😢",
            "Empty circle! Nothing to dequeue 🔵",
            "Queue is taking a nap! 💤",
            "All gone! The circle mourns 🪦",
            "Queue vanished like a donut hole 🍩"
        ]))
        return
    cq[cq_front]=None
    if cq_front==cq_rear:
        cq_front=cq_rear=-1
        messagebox.showinfo("Circular Queue", random.choice([
            "Circular Queue is now empty! Yay? 🎉",
            "All gone! Circle of emptiness 🌀",
            "Queue emptied... mission complete 🏁"
        ]))
    else:
        cq_front=(cq_front+1)%CQ_CAP
    draw_data(cq, mode='cqueue')

# ----------------------- GENERATE DATA -----------------------
def generate_data(size=20,min_val=5,max_val=100, mode='horizontal'):
    global data, stack_items, queue_items, cq, cq_front, cq_rear

    if mode=='stack':
        size = min(size, STACK_CAP)
        stack_items = [random.randint(min_val,max_val) for _ in range(size)]
        draw_data(stack_items, mode='stack')
    elif mode=='queue':
        size = min(size, QUEUE_CAP, 10)
        queue_items = [random.randint(min_val,max_val) for _ in range(size)]
        draw_data(queue_items, mode='queue')
    elif mode=='cqueue':
        size = min(size, CQ_CAP, 10)
        cq = [None]*CQ_CAP
        for i in range(size):
            cq[i] = random.randint(min_val,max_val)
        cq_front, cq_rear = (0, size-1) if size>0 else (-1,-1)
        draw_data(cq, mode='cqueue')
    else:
        size = min(size, 20)
        data = [random.randint(min_val,max_val) for _ in range(size)]
        draw_data(data)

# ----------------------- RUN -----------------------
def run_algorithm():
    c=algo_menu.get()
    try: val=int(op_value_entry.get()) if op_value_entry.get() else None
    except: val=None
    
    if c.startswith("1."): bubble_sort()
    elif c.startswith("2."): insertion_sort()
    elif c.startswith("3."): selection_sort()
    elif c.startswith("4."): merge_sort(); draw_data(data)
    elif c.startswith("5."): draw_data(queue_items, mode='queue')
    elif c.startswith("6."): draw_data(cq, mode='cqueue')
    elif c.startswith("7."): draw_data(stack_items, mode='stack')

# ----------------------- DYNAMIC BUTTONS -----------------------
queue_buttons=[]
cqueue_buttons=[]
stack_buttons=[]

def update_operation_buttons(event=None):
    for b in queue_buttons + cqueue_buttons + stack_buttons:
        b.destroy()
    queue_buttons.clear(); cqueue_buttons.clear(); stack_buttons.clear()

    algo = algo_menu.get()
    if algo.startswith("5."):  # Queue
        for i,(txt,cmd) in enumerate([
            ("Enqueue", lambda: enqueue(int(op_value_entry.get()) if op_value_entry.get().isdigit() else None)),
            ("Dequeue", dequeue)
        ]):
            b=tk.Button(ops_row,text=txt,width=10,command=cmd); b.grid(row=0,column=i+1,padx=6)
            queue_buttons.append(b)
    elif algo.startswith("6."):  # Circular Queue
        for i,(txt,cmd) in enumerate([
            ("C-Enqueue", lambda: circular_enqueue(int(op_value_entry.get()) if op_value_entry.get().isdigit() else None)),
            ("C-Dequeue", circular_dequeue)
        ]):
            b=tk.Button(ops_row,text=txt,width=10,command=cmd); b.grid(row=0,column=i+1,padx=6)
            cqueue_buttons.append(b)
    elif algo.startswith("7."):  # Stack
        for i,(txt,cmd) in enumerate([
            ("Push", lambda: push(int(op_value_entry.get()) if op_value_entry.get().isdigit() else None)),
            ("Pop", pop)
        ]):
            b=tk.Button(ops_row,text=txt,width=10,command=cmd); b.grid(row=0,column=i+1,padx=6)
            stack_buttons.append(b)

# ----------------------- GUI -----------------------
root=tk.Tk()
root.title("Algorithm Visualizer")
root.geometry("900x700")

# --- Controls ---
controls=tk.Frame(root,pady=10); controls.pack(fill=tk.X)
algo_frame=tk.LabelFrame(controls,text="Algorithms"); algo_frame.pack(side=tk.LEFT,padx=10)
algo_menu=ttk.Combobox(algo_frame,width=38,values=[
    "1. Bubble Sort","2. Insertion Sort","3. Selection Sort","4. Merge Sort",
    "5. Queue","6. Circular Queue","7. Stack"])
algo_menu.grid(row=0,column=0,padx=6,pady=6); algo_menu.set("1. Bubble Sort")
algo_menu.bind("<<ComboboxSelected>>", update_operation_buttons)

options_frame=tk.Frame(controls); options_frame.pack(side=tk.LEFT,padx=20)
speed_scale=tk.Scale(options_frame,from_=0.02,to=0.6,length=300,digits=3,resolution=0.02,orient=tk.HORIZONTAL,label="Speed (higher = slower)")
speed_scale.set(0.12); speed_scale.grid(row=0,column=0,padx=6)
tk.Label(options_frame,text="Bar Color:").grid(row=1,column=0,sticky='w',padx=6)
color_var=ttk.Combobox(options_frame,values=["blue","purple","orange","yellow","pink","cyan","magenta"])
color_var.grid(row=1,column=0,padx=90); color_var.set("blue")

# --- Data entries ---
ops_frame=tk.Frame(controls); ops_frame.pack(side=tk.RIGHT,padx=10)
size_entry,min_entry,max_entry=tk.Entry(ops_frame,width=5),tk.Entry(ops_frame,width=5),tk.Entry(ops_frame,width=5)
for e,v in zip([size_entry,min_entry,max_entry],["20","5","100"]): e.insert(0,v)
tk.Label(ops_frame,text="Data size:").grid(row=0,column=0); size_entry.grid(row=0,column=1)
tk.Label(ops_frame,text="Min:").grid(row=0,column=2); min_entry.grid(row=0,column=3)
tk.Label(ops_frame,text="Max:").grid(row=0,column=4); max_entry.grid(row=0,column=5)

# --- Buttons ---
btn_frame=tk.Frame(root,pady=6); btn_frame.pack()
tk.Button(btn_frame,text="Generate Data",
          command=lambda: generate_data(int(size_entry.get()),int(min_entry.get()),int(max_entry.get()),
                                        'stack' if algo_menu.get().startswith('7.') 
                                        else 'queue' if algo_menu.get().startswith('5.') 
                                        else 'cqueue' if algo_menu.get().startswith('6.') 
                                        else 'horizontal'),
          bg="lightgreen").grid(row=0,column=0,padx=8)
tk.Button(btn_frame,text="Start / Run",command=run_algorithm,bg="lightblue").grid(row=0,column=1,padx=8)

# --- Dynamic operation buttons ---
ops_row=tk.Frame(root,pady=6); ops_row.pack()
op_value_entry=tk.Entry(ops_row,width=8); op_value_entry.grid(row=0,column=0,padx=6)

# --- Canvas ---
canvas=tk.Canvas(root,width=700,height=350,bg="white"); canvas.pack(pady=10)
tk.Label(root,text="Tips: Select algorithm, adjust speed, use operation buttons if applicable.").pack(pady=6)

# Initialize dynamic buttons
update_operation_buttons()

root.mainloop()