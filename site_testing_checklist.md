# The Dao of Life - Live Site Testing Checklist

## 🎉 Congratulations! Your Site is Live!

**URL:** https://web-production-f05ad.up.railway.app

The site is loading successfully! Now let's make sure everything works properly.

---

## Critical Testing (Do This First - 15 minutes)

### Authentication Tests

**Test 1: Register New User**
1. [ ] Go to https://web-production-f05ad.up.railway.app
2. [ ] Click "Register" or "Sign Up"
3. [ ] Fill out form with test email (use a real email you can access)
4. [ ] Submit registration
5. [ ] Should redirect to login or homepage
6. [ ] Verify you're logged in (check for username in nav)

**Test 2: Log In with Admin**
1. [ ] Log out if logged in
2. [ ] Go to login page
3. [ ] Enter your admin credentials
4. [ ] Should successfully log in
5. [ ] Check if you have admin menu/options

**Test 3: Log Out**
1. [ ] Click logout button
2. [ ] Should redirect to home
3. [ ] Verify you're logged out (no username showing)

### Forum Tests

**Test 4: View Forum**
1. [ ] Navigate to Community → Forum (or /community/forum)
2. [ ] Page loads without errors
3. [ ] Can see categories
4. [ ] Can see any existing threads (if any)

**Test 5: Create Forum Thread**
1. [ ] Click "Create Thread" or "New Discussion"
2. [ ] Fill out:
   - Title: "Welcome to our community!"
   - Category: Weekly Reflection
   - Content: "This is our first discussion. What brought you here?"
3. [ ] Submit
4. [ ] Should redirect to thread view
5. [ ] Thread appears in forum list

**Test 6: Reply to Thread**
1. [ ] Open the thread you created
2. [ ] Write a reply: "Thanks for joining!"
3. [ ] Submit
4. [ ] Reply appears below original post

### Events Tests

**Test 7: View Events**
1. [ ] Navigate to Community → Events (or /community/events)
2. [ ] Page loads without errors
3. [ ] Can see event list (empty or populated)

**Test 8: Create Event**
1. [ ] Click "Create Event" or "New Event"
2. [ ] Fill out:
   - Title: "Welcome Virtual Meetup"
   - Description: "Our first community gathering!"
   - Type: Virtual
   - Date: Choose tomorrow
   - Time: Choose evening time
   - Virtual Link: https://meet.google.com/test (or any URL)
3. [ ] Submit
4. [ ] Event appears in list

**Test 9: RSVP to Event**
1. [ ] Open the event you created
2. [ ] Click RSVP "Attending"
3. [ ] Should show you're registered
4. [ ] Attendee count should increase

---

## Mobile Testing (10 minutes)

### Test on Your Phone

1. [ ] Visit site on mobile browser
2. [ ] Navigation menu works (hamburger menu?)
3. [ ] Can log in on mobile
4. [ ] Can read forum posts
5. [ ] Can create new post (typing works well)
6. [ ] Text is readable (not too small)
7. [ ] Buttons are tappable (not too small)
8. [ ] Images load properly

---

## Secondary Features Testing (20 minutes)

### Journal Tests

**Test 10: Create Journal Entry**
1. [ ] Navigate to Journal section
2. [ ] Click "New Entry"
3. [ ] Fill out:
   - Content: "My first reflection on mindfulness"
   - Practice type: Meditation
   - Privacy: Private (or Public)
4. [ ] Submit
5. [ ] Entry appears in your journal list

**Test 11: View Practice Streak**
1. [ ] Check if practice streak counter exists
2. [ ] Should show 1 day (from your entry)

### Wisdom Exchange Tests

**Test 12: Share Wisdom**
1. [ ] Navigate to Wisdom Exchange
2. [ ] Click "Share Wisdom" or similar
3. [ ] Add a quote:
   - Content: "The journey of a thousand miles begins with a single step"
   - Source: Lao Tzu
4. [ ] Submit
5. [ ] Appears in wisdom feed

**Test 13: Upvote Wisdom**
1. [ ] Click upvote on your wisdom post
2. [ ] Counter should increase
3. [ ] Button should indicate you've upvoted

### Creative Gallery Tests

**Test 14: Share Creative Work**
1. [ ] Navigate to Creative Corner
2. [ ] Click "Share Work" or "Upload"
3. [ ] Try uploading:
   - Type: Poetry
   - Title: "Morning Reflection"
   - Content: A short poem
4. [ ] Submit
5. [ ] Work appears in gallery

### Resource Library Tests

**Test 15: Browse Resources**
1. [ ] Navigate to Resources
2. [ ] Can see resource list
3. [ ] Can filter by category

**Test 16: Submit Resource**
1. [ ] Click "Submit Resource"
2. [ ] Fill out:
   - Title: "Introduction to Stoicism"
   - Type: Article
   - URL: https://example.com/stoicism
   - Description: Brief description
3. [ ] Submit
4. [ ] Should appear (possibly pending approval)

---

## Admin Panel Testing (15 minutes)

### Admin Dashboard

**Test 17: Access Admin Panel**
1. [ ] Log in as admin
2. [ ] Look for "Admin" link in navigation
3. [ ] Should access admin dashboard
4. [ ] Can see user count, post count, etc.

**Test 18: Moderate Content**
1. [ ] Look for moderation section
2. [ ] Can see flagged content (if any)
3. [ ] Can approve/reject user submissions
4. [ ] Can pin/unpin forum threads

**Test 19: Manage Users**
1. [ ] Navigate to Users section in admin
2. [ ] Can see list of users
3. [ ] Can view user details
4. [ ] Can change user roles (test carefully!)

---

## Error Testing (10 minutes)

### Test Error Handling

**Test 20: 404 Page**
1. [ ] Visit https://web-production-f05ad.up.railway.app/nonexistent-page
2. [ ] Should show custom 404 error page (not generic error)
3. [ ] Has link back to home

**Test 21: Form Validation**
1. [ ] Try creating forum post with empty title
2. [ ] Should show error message
3. [ ] Form should not submit

**Test 22: Login with Wrong Password**
1. [ ] Try logging in with wrong password
2. [ ] Should show "invalid credentials" message
3. [ ] Should not crash

---

## Performance Testing (5 minutes)

### Load Times

**Test 23: Page Speed**
1. [ ] Open browser dev tools (F12)
2. [ ] Navigate to different pages
3. [ ] Check load times (should be < 3 seconds)
4. [ ] Check for any console errors (red text)

**Test 24: Multiple Tabs**
1. [ ] Open site in 3 different tabs
2. [ ] Navigate in each tab
3. [ ] No crashes or weird behavior

---

## Security Testing (5 minutes)

**Test 25: HTTPS**
1. [ ] Check URL bar - should show lock icon 🔒
2. [ ] Click lock - should say "Secure Connection"
3. [ ] Railway provides SSL automatically

**Test 26: CSRF Protection**
1. [ ] Check forms have csrf_token (view source)
2. [ ] Flask-WTF provides this automatically

**Test 27: Password Security**
1. [ ] Try viewing user passwords in database
2. [ ] Should be hashed (not plain text)
3. [ ] Check Railway logs - no passwords visible

---

## Issues to Look For

### Common Problems After Deployment

**Database Issues:**
- [ ] "Database connection failed" - Check DATABASE_URL
- [ ] "Table doesn't exist" - Run `flask db upgrade`
- [ ] Data not persisting - Check Neon connection

**Static File Issues:**
- [ ] CSS not loading - Check paths in base.html
- [ ] Images not showing - Check /static/img/ paths
- [ ] Styles look broken - CSS file not found

**Authentication Issues:**
- [ ] Can't log in - Check SECRET_KEY is set
- [ ] Sessions not persisting - Check session config
- [ ] "Unauthorized" errors - Check Flask-Login setup

**Form Issues:**
- [ ] Forms not submitting - Check CSRF token
- [ ] Validation errors - Check WTForms validators
- [ ] Upload fails - Check MAX_CONTENT_LENGTH

---

## Things That Should Work

Based on your codebase, these features should be functional:

✅ User registration and login
✅ Forum threads and replies
✅ Community events with RSVP
✅ Private journals
✅ Wisdom sharing with upvotes
✅ Creative works gallery
✅ Resource library
✅ Admin moderation panel
✅ User roles (admin, moderator, user)
✅ Email newsletter signup
✅ Contact form
✅ About/Mission pages

---

## Railway Monitoring

### Check Your Deployment

1. **View Logs:**
   - Railway dashboard → Your service
   - Click "Deployments" → Latest deployment
   - Click "View Logs"
   - Look for any errors (red text)

2. **Check Resource Usage:**
   - Railway dashboard → Metrics
   - CPU usage (should be low)
   - Memory usage (should be under limit)
   - Request count

3. **Monitor Costs:**
   - Railway dashboard → Usage
   - Should show $0 (using free credit)
   - Watch to ensure staying under $5/month

---

## Quick Fixes for Common Issues

### If Forum Doesn't Load:
```python
# Check community blueprint is registered
# In app/__init__.py, should have:
app.register_blueprint(community_bp)
```

### If Login Doesn't Work:
```bash
# Check admin user exists
railway run flask shell
>>> from app.models import User
>>> User.query.filter_by(role='admin').first()
```

### If Database Errors:
```bash
# Re-run migrations
railway run flask db upgrade
```

### If Static Files Don't Load:
```python
# Check config.py has correct paths
# Static files should be in app/static/
```

---

## Next Steps After Testing

### If Everything Works:
1. ✅ **Create welcome content**
   - First forum post
   - First event
   - Update About page

2. ✅ **Invite 5-10 beta testers**
   - Share URL with friends/family
   - Ask them to test and give feedback

3. ✅ **Monitor daily**
   - Check Railway logs for errors
   - Respond to user issues quickly

### If Issues Found:
1. 🐛 **Document the bug**
   - What happened?
   - What were you doing?
   - What error message?

2. 🐛 **Check Railway logs**
   - Look for error stack trace
   - Note the timestamp

3. 🐛 **Fix and redeploy**
   - Fix in code
   - Push to GitHub
   - Railway auto-deploys

---

## Success Metrics

### Week 1 Goals:
- [ ] 5-10 registered users
- [ ] 10+ forum posts
- [ ] 1+ event created
- [ ] Zero critical bugs
- [ ] Positive feedback from testers

### What to Measure:
- User registrations (via admin panel)
- Daily active users
- Forum posts per day
- Event RSVPs
- Time spent on site

---

## Report Back

After testing, let me know:

1. **What works?** ✅
2. **What's broken?** 🐛
3. **What's confusing?** 🤔
4. **What do you want to improve first?** 🎯

Then we can tackle the next priority together!

---

## Quick Test Script

Run through these in 15 minutes for a quick health check:

1. Load homepage ✓
2. Register new user ✓
3. Create forum post ✓
4. Create event ✓
5. Test on mobile ✓
6. Check admin panel ✓
7. View Railway logs ✓

If all 7 pass, you're good to invite beta testers!
