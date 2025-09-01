# 🔐 Secure Information Retrieval System (SIRS)

> A cloud-based, privacy-preserving document storage and search platform with semantic and encrypted search capabilities.

---

## 📘 Overview

**SIRS** (Secure Information Retrieval System) is a secure, scalable platform that enables users to **upload**, **store**, **search**, and **retrieve encrypted documents** without exposing sensitive content or search queries.

Built with advanced **NLP, encryption, and access control**, SIRS supports **fuzzy and semantic search**, **role-based access (RBAC)**, and **chat-based querying**, all within a clean, modern web interface.

---

## ⚙️ Key Features

### 🔐 Security & Access Control

* Role-Based Access Control (RBAC): Admin, Data Owner, General User
* Optional Attribute-Based Encryption (ABE)
* End-to-end AES encryption of documents

### 🧠 Privacy-Preserving Search

* Fuzzy & semantic search using embeddings (MiniLM / BERT)
* Secure trapdoor queries using HMAC/SHA
* No plaintext search or indexing exposed

### 📂 Document Management

* Upload and encrypt files securely
* Automated keyword extraction & preprocessing
* Store on cloud (AWS S3 or MongoDB) with metadata in PostgreSQL/MySQL

### 🔍 Intelligent Retrieval

* Keyword & semantic ranking using BM25 / FAISS
* Preview before decryption (RBAC-verified)
* Client- or server-side decryption depending on role

### 💬 Chat-Based Query Interface

* Natural language search experience
* Semantic parsing + fallback to keyword search
* Optional GPT integration for guidance/suggestions

### 📊 Admin Dashboard

* Monitor user activity, storage usage, and query logs
* View system metrics: search latency, precision, recall
* Export audit logs

---

## 🏗️ Tech Stack

| Layer      | Tech                                |
| ---------- | ----------------------------------- |
| Frontend   | React or Next.js + Tailwind CSS     |
| Backend    | Django + Django REST Framework      |
| Encryption | AES, HMAC, SHA-256                  |
| Embeddings | SentenceTransformers (MiniLM, BERT) |
| Search     | FAISS + BM25/TF-IDF                 |
| Storage    | AWS S3 / MongoDB + PostgreSQL       |
| Auth       | JWT + Django AllAuth                |
| NLP Tools  | spaCy, WordNet, NLTK                |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Levi-Chinecherem/sirs.git
cd sirs
```

### 2. Set Up Backend

```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Set Up Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Environment Variables

Create a `.env` file in both `frontend/` and `backend/` directories and configure:

```env
# Backend .env
SECRET_KEY=your-secret
DATABASE_URL=...
AWS_ACCESS_KEY=...
FAISS_INDEX_PATH=...

# Frontend .env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 🧪 Testing

* Use the **Cranfield Dataset** for relevance testing
* Simulate multi-user search sessions
* Validate RBAC enforcement and encrypted query processing

---

## 🧠 Sample Use Cases

* 🔍 Researcher securely searching institution-owned archives
* 🏛️ Government entity enabling controlled access to sensitive records
* 🎓 University storing academic papers with confidential metadata

---

## 🔒 Security Principles

* **End-to-End Encryption**: AES-256 for documents, HMAC-SHA for queries
* **Zero Trust Search**: Queries are encrypted, no raw text ever stored
* **Fine-Grained Access**: Role enforcement per document or action
* **Audit Logging**: All sensitive actions are recorded and visible to Admins

---

## 📌 Roadmap

* [x] RBAC with role-restricted decryption
* [x] Keyword & semantic search
* [x] FAISS-powered vector ranking
* [x] File upload and secure metadata indexing
* [ ] Chat-based query interface (MVP)
* [ ] ABE integration (optional)
* [ ] GDPR-compliant logging

---

## 👥 Contributing

Pull requests and community contributions are welcome!

1. Fork the repo
2. Create your branch: `git checkout -b feature/awesome-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/awesome-feature`
5. Open a pull request
