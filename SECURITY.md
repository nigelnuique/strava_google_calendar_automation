# Security Guidelines

## 🚨 **IMMEDIATE ACTIONS REQUIRED**

### 1. **Secure Your API Credentials**
Your `.env` file contains real API credentials. Take these steps immediately:

```bash
# 1. Regenerate all API tokens
# - Go to Strava Developer Console and regenerate your tokens
# - Go to Google Cloud Console and regenerate OAuth credentials

# 2. Clear sensitive data from terminal history
# Windows PowerShell:
Clear-History
Remove-Item (Get-PSReadlineOption).HistorySavePath

# 3. Consider using a secure credential manager
```

### 2. **Environment File Security**
Your `.env` file should **NEVER** contain real credentials during development:

```env
# ❌ DON'T DO THIS
STRAVA_CLIENT_SECRET=real_secret_here

# ✅ DO THIS INSTEAD
STRAVA_CLIENT_SECRET=your_strava_client_secret_here
```

## 🔒 **Security Best Practices**

### **For Local Development**
1. **Use placeholder values** in `.env` files
2. **Store real credentials** in your system's secure credential store
3. **Clear terminal history** after viewing credentials
4. **Use environment-specific** credential files

### **For Production (GitHub Actions)**
1. **Use GitHub Secrets** for all sensitive data
2. **Rotate credentials** regularly
3. **Monitor secret usage** in GitHub Actions logs
4. **Use least-privilege** API permissions

### **General Security**
1. **Never commit** `.env` files with real credentials
2. **Use short-lived tokens** when possible
3. **Monitor for credential leaks** in logs
4. **Regularly audit** your security practices

## 🛡️ **Security Checklist**

- [ ] All API credentials regenerated
- [ ] `.env` file contains only placeholder values
- [ ] Terminal history cleared
- [ ] GitHub secrets properly configured
- [ ] No credentials in source code
- [ ] Error messages don't leak sensitive data
- [ ] Regular security audits scheduled

## 📞 **What to Do if Credentials Are Compromised**

1. **Immediately revoke** all affected tokens
2. **Generate new credentials** from API providers
3. **Update GitHub secrets** with new values
4. **Check logs** for unauthorized usage
5. **Review recent activity** in connected accounts

## 🔍 **Security Audit Commands**

```bash
# Check for potential credential leaks
git log --all --grep="token\|secret\|password" --oneline
git log --all -S "secret" --oneline
git log --all -S "token" --oneline

# Check current ignored files
git status --ignored

# Verify no sensitive files are tracked
git ls-files | grep -E "\.(env|json)$"
```

## 🚨 **Emergency Contacts**

If you discover a security breach:
1. **Strava**: Revoke tokens at https://developers.strava.com/
2. **Google**: Revoke access at https://myaccount.google.com/permissions
3. **GitHub**: Review and rotate secrets in repository settings

---

**Remember**: Security is an ongoing process, not a one-time setup. Regular audits and updates are essential. 