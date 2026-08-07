// Custom JavaScript for UK Portfolio Admin Dashboard
document.addEventListener("DOMContentLoaded", function () {
    console.log("Modern Admin Dashboard template loaded successfully.");

    // Dynamically rename "General" tab to "Title Section" on all tabbed change forms
    const renameGeneralTab = () => {
        const tabLinks = document.querySelectorAll(".nav-tabs .nav-link, .nav-tabs a");
        tabLinks.forEach(function (tab) {
            if (tab.textContent.trim() === "General") {
                tab.textContent = "Title Section";
            }
        });
    };

    // Run immediately
    renameGeneralTab();

    // Run again in case tabs are rendered dynamically later
    setTimeout(renameGeneralTab, 100);

    // Dynamically append Logout button to the bottom of the sidebar list
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
});
