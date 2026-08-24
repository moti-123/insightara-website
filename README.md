# Insightara Website

Full responsive website with a Django backend + admin panel for **Insightara**
(founder, co-founder, team, projects, client contact form).

## Kya kya bana hai

- **Public site**: Home page (hero, about, founder, co-founder, team grid, projects, contact form) + Projects page
- **Admin panel** (`/admin/`) — Django's built-in admin, customized:
  - `TeamMember` model — Founder/Co-Founder/Team ke photos, bio, job title, order
  - `Project` model — portfolio items, kisi bhi staff member se add ho sakte hain
  - `ContactMessage` model — client contact form ke messages yahan aate hain
- **Role-based access**:
  - **Founder** = Django *superuser* — sab kuch control karta hai, naye users bana sakta hai
  - **Co-Founder** = staff user, "Co-Founder" group mein — team + projects manage kar sakta hai
  - **Team Member** = staff user, "Team Member" group mein — sirf projects add/edit kar sakta hai

## Local setup (apne laptop pe chalane ke liye)

```bash
# 1. Virtual environment banao
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Dependencies install karo
pip install -r requirements.txt

# 3. Database setup
python manage.py migrate

# 4. Permission groups banao (Co-Founder / Team Member roles)
python manage.py setup_roles

# 5. Apna Founder account banao (ye superuser hoga)
python manage.py createsuperuser

# 6. Server chalao
python manage.py runserver
```

Ab `http://127.0.0.1:8000/` pe site aur `http://127.0.0.1:8000/admin/` pe admin panel khulega.

## Admin panel se kaise kaam lena hai (Founder ke liye)

1. `/admin/` pe login karo apne superuser account se.
2. **Team Members** section mein jaake:
   - Apni entry banao — `role_category = Founder`
   - Co-founder ki entry banao — `role_category = Co-Founder`
   - Baaki team ki entries — `role_category = Team Member`
3. **Naya team member (jo website bhi use kar sake) add karne ke liye:**
   - Django admin mein "Users" section > "Add user"
   - Username/password set karo, **"Staff status" ka box tick karo** (warna wo login nahi kar payega)
   - Us user ko "Co-Founder" ya "Team Member" group mein daalo
   - Phir "Team Members" mein unki public profile (photo, bio) bhi add kar dena
4. **Projects** add karne ke liye — "Projects" section mein "Add Project" — title, summary, tools, image daal do. Status "Published" rakhna taake site pe dikhe.
5. **Client Inquiries** — jab koi contact form fill karega, wo yahan aayega. Read karke `is_read` tick kar sakte ho.

## Free hosting pe deploy karna (Render.com)

1. Is project ko GitHub repo mein push karo.
2. [render.com](https://render.com) pe free account banao, GitHub se connect karo.
3. "New +" → "Blueprint" → apna repo select karo (ye `render.yaml` file khud detect ho jayegi — free web service + free Postgres database dono create ho jayenge).
4. Deploy hone ke baad, Render ke **Shell** tab se ye commands ek baar chalao:
   ```bash
   python manage.py setup_roles
   python manage.py createsuperuser
   ```
5. Bas — tumhari site `https://insightara-site.onrender.com` (ya jo bhi naam ho) pe live ho jayegi.

**Note:** Render ka free tier ~15 min inactivity ke baad "sleep" ho jata hai aur agli request pe 30-50 second lagti hai jagne mein. Client demo se pehle ek baar site khol lena taake wo "warm" ho jaye. Paid plan ($7/month) se ye issue nahi hota.

## Design

Palette: deep navy (`#0B1F3A`) + gold (`#C9A227`) + ivory (`#F7F5EF`) — Insightara ke existing brand colors ke saath match karta hai. Fonts: Fraunces (headings) + Inter (body) + JetBrains Mono (labels/data).

## Aage kya add kar sakte ho

- Email notifications jab naya contact message aaye (Django's `EMAIL_BACKEND` setup se)
- Custom domain connect karna (Render mein free hai, sirf DNS point karna hota hai)
- Blog/case-studies section
- Google Analytics ya Plausible tracking
