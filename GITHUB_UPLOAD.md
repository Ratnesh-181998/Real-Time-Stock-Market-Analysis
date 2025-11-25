# How to Upload to GitHub

Follow these steps to upload this project to your GitHub repository.

## 1. Initialize Git
Open your terminal in the project folder (`Real-Time Stock Analysis`) and run:

```bash
git init
```

## 2. Add Files
Add all files to the staging area (the `.gitignore` file will ensure unnecessary files like `kafka_local` and `venv` are excluded):

```bash
git add .
```

## 3. Commit Changes
Commit the files with a message:

```bash
git commit -m "Initial commit: Real-Time Stock Analysis System with Kafka and LSTM"
```

## 4. Create Repository on GitHub
1.  Go to [GitHub.com](https://github.com) and sign in.
2.  Click the **+** icon in the top right and select **New repository**.
3.  Name it `real-time-stock-analysis`.
4.  Click **Create repository**.

## 5. Link and Push
Copy the commands provided by GitHub (under "…or push an existing repository from the command line") and run them:

```bash
# Replace 'yourusername' with your actual GitHub username
git remote add origin https://github.com/yourusername/real-time-stock-analysis.git
git branch -M main
git push -u origin main
```

## ✅ Done!
Your project is now live on GitHub.
