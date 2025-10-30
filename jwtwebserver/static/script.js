document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
        // 토큰을 로컬스토리지에 저장
        localStorage.setItem("jwt_token", data.token);
        alert("로그인 성공!");
        window.location.href = "/protected";
    } else {
        alert("로그인 실패: " + data.message);
    }
});
