// Custom JavaScript for UK Portfolio Admin Dashboard
document.addEventListener("DOMContentLoaded", function () {
    console.log("Modern Admin Dashboard template loaded successfully.");

    // 1. Dynamically rename "General" tab to "Title Section" on all tabbed change forms
    const renameGeneralTab = () => {
        const tabLinks = document.querySelectorAll(".nav-tabs .nav-link, .nav-tabs a");
        tabLinks.forEach(function (tab) {
            if (tab.textContent.trim() === "General") {
                tab.textContent = "Title Section";
            }
        });
    };
    renameGeneralTab();
    setTimeout(renameGeneralTab, 100);

    // 2. Dynamically append Logout button to the bottom of the sidebar list
    const sidebarNav = document.querySelector("ul.nav-sidebar");
    if (sidebarNav) {
        if (!document.getElementById("sidebar-logout-item")) {
            const logoutLi = document.createElement("li");
            logoutLi.className = "nav-item nav-item-logout";
            logoutLi.id = "sidebar-logout-item";

            logoutLi.innerHTML = `
                <a href="/dashboard/logout/" class="nav-link">
                    <i class="nav-icon fas fa-sign-out-alt"></i>
                    <p>Log out</p>
                </a>
            `;
            sidebarNav.appendChild(logoutLi);
        }
    }

    // 3. Helper utilities: HTML escape & initial
    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function getInitial(name) {
        if (!name) return 'M';
        const clean = name.trim().replace(/^[^a-zA-Z0-9]+/, '');
        return clean ? clean.charAt(0).toUpperCase() : 'M';
    }

    // 4. Synthesizer Audio Chime for live incoming email notification
    function playNotificationChime() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            const now = ctx.currentTime;

            // Two-tone pleasant notification chime (D5 -> A5)
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(587.33, now);
            gain1.gain.setValueAtTime(0, now);
            gain1.gain.linearRampToValueAtTime(0.12, now + 0.04);
            gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.30);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(now);
            osc1.stop(now + 0.30);

            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(880, now + 0.12);
            gain2.gain.setValueAtTime(0, now + 0.12);
            gain2.gain.linearRampToValueAtTime(0.15, now + 0.16);
            gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.50);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(now + 0.12);
            osc2.stop(now + 0.50);
        } catch (e) {
            // Audio context silently ignored if restricted by browser policy
        }
    }

    // 5. Live Floating Toast for incoming emails without page reload
    function showLiveEmailToast(msg) {
        if (!msg) return;

        let container = document.getElementById("emailLiveToastContainer");
        if (!container) {
            container = document.createElement("div");
            container.id = "emailLiveToastContainer";
            container.className = "email-live-toast-container";
            document.body.appendChild(container);
        }

        const toast = document.createElement("div");
        toast.className = "email-live-toast";
        const initial = getInitial(msg.sender_name || msg.sender_email);
        const viewUrl = `/dashboard/contactapp/receivedemail/${msg.id}/change/`;

        toast.innerHTML = `
            <div class="toast-avatar-bubble">${initial}</div>
            <div class="toast-text-content">
                <div class="toast-kicker">
                    <span class="toast-kicker-dot"></span> New Email Received
                </div>
                <div class="toast-sender-title" title="${escapeHtml(msg.sender_name || msg.sender_email)}">
                    ${escapeHtml(msg.sender_name || msg.sender_email)}
                </div>
                <div class="toast-subject-snippet" title="${escapeHtml(msg.subject)}">
                    ${escapeHtml(msg.subject)}
                </div>
                <div class="toast-action-row">
                    <a href="${viewUrl}" class="toast-view-btn">
                        <i class="fas fa-envelope-open-text me-1"></i> Read Email
                    </a>
                    <a href="/dashboard/email/inbox/?id=${msg.id}" class="btn btn-xs btn-outline-secondary py-0 px-2" style="font-size: 0.70rem; border-radius: 5px;">
                        Webmail
                    </a>
                </div>
            </div>
            <button type="button" class="toast-close-btn" aria-label="Close">&times;</button>
        `;

        const closeBtn = toast.querySelector(".toast-close-btn");
        const dismissToast = () => {
            toast.classList.add("toast-hiding");
            setTimeout(() => toast.remove(), 350);
        };

        closeBtn.addEventListener("click", dismissToast);
        setTimeout(dismissToast, 8500);

        container.appendChild(toast);
    }

    // 6. Inject Hostinger Email Notification Bell in Top Navbar
    function setupTopNavNotification() {
        const navbarRight = document.querySelector(".main-header .navbar-nav.ms-auto") ||
                            document.querySelector(".main-header .navbar-nav.ml-auto") ||
                            document.querySelector(".navbar-nav.ms-auto") ||
                            document.querySelector(".navbar-nav.ml-auto");
        
        if (!navbarRight) return;
        if (document.getElementById("topNavNotificationDropdown")) return;

        const li = document.createElement("li");
        li.className = "nav-item dropdown";
        li.id = "topNavNotificationDropdown";

        li.innerHTML = `
            <a class="nav-link notification-bell-link" href="#" id="topNavBellBtn" title="Hostinger Mail Notifications" aria-expanded="false">
                <i class="far fa-bell" style="font-size: 1.12rem;"></i>
                <span class="navbar-badge-notify" id="topNavUnreadBadge" style="display: none;">0</span>
            </a>
            <div class="dropdown-menu dropdown-menu-end notification-dropdown-menu" id="topNavNotificationMenu">
                <!-- Dropdown Header -->
                <div class="d-flex align-items-center justify-content-between px-3 py-2.5 border-bottom bg-white">
                    <div class="d-flex align-items-center gap-2">
                        <i class="fas fa-inbox text-primary"></i>
                        <span class="fw-bold text-dark" style="font-size: 0.90rem;">Incoming Mail</span>
                        <span class="badge bg-danger text-white" id="headerUnreadBadge" style="font-size: 0.65rem; border-radius: 9999px; padding: 2px 7px; display: none;">0 unread</span>
                    </div>
                    <button type="button" class="btn btn-sm d-flex align-items-center gap-1" id="topNavSyncBtn" title="Check Hostinger IMAP now" style="font-size: 0.72rem; border-radius: 9999px; text-transform: none !important; font-weight: 600; padding: 3px 10px; background: #f8fafc; border: 1px solid #e2e8f0; color: #475569;">
                        <i class="fas fa-sync-alt" id="topNavSyncIcon"></i>
                        <span>Sync</span>
                    </button>
                </div>

                <!-- Notifications List Container -->
                <div id="topNavNotificationList" style="max-height: 330px; overflow-y: auto;">
                    <div class="p-3 text-center text-muted">
                        <div class="spinner-border spinner-border-sm text-primary mb-1" role="status"></div>
                        <div style="font-size: 0.75rem;">Connecting to Hostinger...</div>
                    </div>
                </div>

                <!-- Dropdown Footer -->
                <div class="p-2 border-top bg-light d-flex align-items-center gap-2" style="background: #f8fafc !important;">
                    <a href="/dashboard/contactapp/receivedemail/" class="btn btn-sm w-50 d-flex align-items-center justify-content-center gap-1.5" style="text-transform: none !important; font-weight: 600; font-size: 0.78rem; border-radius: 0.5rem; padding: 6px 10px; color: #334155; background: #ffffff; border: 1px solid #cbd5e1; text-decoration: none;">
                        <i class="fas fa-list text-muted"></i> All Received
                    </a>
                    <a href="/dashboard/email/inbox/" class="btn btn-sm w-50 d-flex align-items-center justify-content-center gap-1.5 text-white" style="text-transform: none !important; font-weight: 600; font-size: 0.78rem; border-radius: 0.5rem; padding: 6px 10px; background: linear-gradient(135deg, #1a4674 0%, #0d233a 100%); border: none; box-shadow: 0 2px 6px rgba(26,70,116,0.25); text-decoration: none;">
                        <i class="fas fa-columns"></i> Webmail Inbox
                    </a>
                </div>
            </div>
        `;

        // Insert before the last item (user profile menu) if possible
        if (navbarRight.children.length > 0) {
            navbarRight.insertBefore(li, navbarRight.lastElementChild);
        } else {
            navbarRight.appendChild(li);
        }

        // Dropdown toggle handler
        const bellBtn = li.querySelector("#topNavBellBtn");
        const menu = li.querySelector("#topNavNotificationMenu");

        bellBtn.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            const isOpen = menu.classList.contains("show");
            if (isOpen) {
                menu.classList.remove("show");
                bellBtn.setAttribute("aria-expanded", "false");
            } else {
                menu.classList.add("show");
                bellBtn.setAttribute("aria-expanded", "true");
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener("click", function (e) {
            if (!li.contains(e.target)) {
                menu.classList.remove("show");
                bellBtn.setAttribute("aria-expanded", "false");
            }
        });

        // Sync button click inside dropdown
        const syncBtn = li.querySelector("#topNavSyncBtn");
        if (syncBtn) {
            syncBtn.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                fetchNotifications(true);
            });
        }
    }

    // 7. Inject Sidebar Unread Count Badge
    function setupSidebarBadge() {
        const inboxLink = document.querySelector('ul.nav-sidebar a[href*="/dashboard/email/inbox/"]') ||
                          document.querySelector('ul.nav-sidebar a[href*="contactapp/receivedemail/"]') ||
                          document.querySelector('a[href*="/dashboard/email/inbox/"]');
        if (!inboxLink) return;

        let badge = document.getElementById("sidebarInboxBadge");
        if (!badge) {
            badge = document.createElement("span");
            badge.id = "sidebarInboxBadge";
            badge.className = "badge sidebar-unread-badge right";
            badge.style.display = "none";

            const pTag = inboxLink.querySelector("p");
            if (pTag) {
                pTag.appendChild(badge);
            } else {
                inboxLink.appendChild(badge);
            }
        }
    }

    // 8. Fetch & Render Email Notifications with Live Auto-Sync
    let isFetching = false;
    let lastUnreadCount = null;

    function fetchNotifications(sync = false) {
        if (isFetching) return;
        isFetching = true;

        const syncIcon = document.getElementById("topNavSyncIcon");
        if (syncIcon && sync) {
            syncIcon.classList.add("fa-spin");
        }

        const url = `/dashboard/email/notifications/?sync=${sync ? 1 : 0}`;

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (!data || !data.success) return;

            const unreadCount = data.unread_count || 0;
            const displayCount = unreadCount > 99 ? '99+' : unreadCount;

            // Detect new incoming emails (without reload)
            const isFirstLoad = (lastUnreadCount === null);
            const hasNewEmails = (!isFirstLoad && (data.synced_new > 0 || unreadCount > lastUnreadCount));
            lastUnreadCount = unreadCount;

            // 1) Update Top Navbar Bell Badge
            const topBadge = document.getElementById("topNavUnreadBadge");
            if (topBadge) {
                if (unreadCount > 0) {
                    topBadge.textContent = displayCount;
                    topBadge.style.display = "inline-block";
                    if (hasNewEmails) {
                        topBadge.classList.add("badge-bounce");
                        setTimeout(() => topBadge.classList.remove("badge-bounce"), 4000);
                    }
                } else {
                    topBadge.style.display = "none";
                }
            }

            // 2) Update Sidebar Badge
            const sidebarBadge = document.getElementById("sidebarInboxBadge");
            if (sidebarBadge) {
                if (unreadCount > 0) {
                    sidebarBadge.textContent = displayCount;
                    sidebarBadge.style.display = "inline-flex";
                    if (hasNewEmails) {
                        sidebarBadge.classList.add("badge-bounce");
                        setTimeout(() => sidebarBadge.classList.remove("badge-bounce"), 4000);
                    }
                } else {
                    sidebarBadge.style.display = "none";
                }
            }

            // 3) Update Header Pill in Dropdown
            const headerPill = document.getElementById("headerUnreadBadge");
            if (headerPill) {
                if (unreadCount > 0) {
                    headerPill.textContent = `${unreadCount} unread`;
                    headerPill.style.display = "inline-block";
                } else {
                    headerPill.style.display = "none";
                }
            }

            // 4) Update Index Page KPI Card (if present)
            const kpiBadge = document.getElementById("metricUnreadEmails");
            if (kpiBadge) {
                kpiBadge.textContent = unreadCount;
            }

            // 5) Render items in Dropdown List
            const listContainer = document.getElementById("topNavNotificationList");
            if (listContainer) {
                if (!data.notifications || data.notifications.length === 0) {
                    listContainer.innerHTML = `
                        <div class="p-4 text-center text-muted">
                            <i class="fas fa-check-circle text-success mb-2" style="font-size: 1.6rem;"></i>
                            <div class="fw-semibold text-dark" style="font-size: 0.85rem;">All Caught Up!</div>
                            <small class="text-muted" style="font-size: 0.75rem;">No unread emails in Hostinger mailbox.</small>
                        </div>
                    `;
                } else {
                    let itemsHtml = '';
                    data.notifications.forEach(item => {
                        const initial = getInitial(item.sender_name || item.sender_email);
                        const detailUrl = `/dashboard/contactapp/receivedemail/${item.id}/change/`;
                        const cleanSnippet = (item.snippet || '').replace(/\[image:[^\]]*\]/gi, '').trim();
                        itemsHtml += `
                            <a href="${detailUrl}" class="notification-item-card">
                                <div class="notification-avatar">${initial}</div>
                                <div style="flex: 1; min-width: 0;">
                                    <div class="d-flex align-items-center justify-content-between mb-0.5">
                                        <span class="fw-bold text-dark text-truncate" style="font-size: 0.80rem; max-width: 170px;">
                                            ${escapeHtml(item.sender_name)}
                                        </span>
                                        <small class="text-muted" style="font-size: 0.68rem; margin-left: 6px; white-space: nowrap;">
                                            ${escapeHtml(item.time_ago)}
                                        </small>
                                    </div>
                                    <div class="text-truncate fw-semibold text-secondary" style="font-size: 0.76rem; margin-bottom: 2px;">
                                        ${item.has_attachment ? '<i class="fas fa-paperclip text-muted me-1" title="Attachment"></i>' : ''}
                                        ${escapeHtml(item.subject)}
                                    </div>
                                    <div class="text-truncate text-muted" style="font-size: 0.70rem; line-height: 1.25;">
                                        ${escapeHtml(cleanSnippet)}
                                    </div>
                                </div>
                            </a>
                        `;
                    });
                    listContainer.innerHTML = itemsHtml;
                }
            }

            // 6) Trigger Live Toast & Chime if new emails received without reload
            if (hasNewEmails) {
                playNotificationChime();
                if (data.new_messages && data.new_messages.length > 0) {
                    data.new_messages.forEach(newMsg => showLiveEmailToast(newMsg));
                } else if (data.notifications && data.notifications.length > 0) {
                    showLiveEmailToast(data.notifications[0]);
                }
            }
        })
        .catch(err => {
            console.warn("Could not fetch email notifications:", err);
        })
        .finally(() => {
            isFetching = false;
            if (syncIcon) {
                syncIcon.classList.remove("fa-spin");
            }
        });
    }

    // Initialize UI Elements
    setupTopNavNotification();
    setupSidebarBadge();

    // Initial Fetch immediately
    fetchNotifications(false);

    // Live background polling (every 15 seconds) for real-time notifications without reload
    setInterval(() => {
        fetchNotifications(false);
    }, 15000);

    // Refresh immediately when user switches tabs back into the window
    window.addEventListener("focus", function () {
        fetchNotifications(false);
    });
});
