# Upload to GitHub

This guide will help you upload the `Real-Time Stock Analysis` project to your GitHub repository.

## 1. Initialize Git
Open your terminal in the project folder (`c:\Users\rattu\Downloads\L-13 & L-14 Kafka\Real-Time Stock Analysis`) and run:

```bash
git init
```

## 2. Add Files
Add all files to the staging area. The `.gitignore` file will automatically exclude large/unnecessary files.

```bash
git add .
```

## 3. Commit Changes
Commit the files with a message:

```bash
git commit -m "Initial commit: Real-Time Stock Analysis System"
```

## 4. Link to Remote Repository
Link your local repository to your GitHub repository:

```bash
git remote add origin https://github.com/Ratnesh-181998/Real-Time-Stock-Market-Analysis.git
```

## 5. Push to GitHub
Push your code to the `main` branch:

```bash
git branch -M main
git push -u origin main
```

---

### Troubleshooting
If you encounter an error like `remote origin already exists`, run this before step 4:
```bash
git remote remove origin
```

If you need to force push (be careful, this overwrites remote history):
```bash
git push -u origin main --force
```
