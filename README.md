# 2025_L1AC-Discrete-Mathematics_Matrix-Tranformation-for-Simple-Game_srzeeke
# How to Play
To **play the game**, you only need to set up your environment correctly.
Your code is complete — nothing is missing. You just need to run it properly.

---

# ✅ **Steps to Play the Game**

## **1. Install Python (if you don’t have it)**

You need Python **3.8 or later**.

Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

Make sure “Add to PATH” is checked during installation.

---

## **2. Install Required Libraries**

Open a terminal / command prompt and run:

```bash
pip install pygame numpy
```

---

## **3. Save the code into a file**

For example:

```
matrix_game.py
```

---

## **4. Run the game**

In the terminal, run:

```bash
python matrix_game.py
```

---

# 🎮 **How to Play**

Once the window opens:

### You will see:

✔ A triangle
✔ Coordinate axes
✔ Buttons on the left
✔ Transformation matrix on the right

### You can click:

* **Translate +X** (move triangle right)
* **Translate –X**
* **Translate +Y**
* **Translate –Y**
* **Rotate +30°**
* **Rotate –30°**
* **Scale +10%**
* **Scale –10%**
* **Reset** (restore original shape)

---

# 🧩 If the game window never opens

Make sure you run Python from your system, NOT inside VS Code’s restricted execution environment.
Also ensure you don’t have multiple Python versions fighting each other.

Run:

```bash
python -m pygame.examples.aliens
```

If that opens a sample pygame game, everything is working.

---

# Features
1. Implements homogeneous transformation matrices for 2D transformations
2. Applies translation, rotation, and scaling transformations
3. Visual feedback with a coordinate system and transformation matrix display
4. Interactive buttons with hover effects
5. Reset functionality to return to the original state

