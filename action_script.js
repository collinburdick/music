function login() {
	var em = req.query.passedEmail, pw = req.query.passedPassword, loginData;
	fireData.authWithPassword({
        email: em,
        password: pw
    }, function (loginError, loginAuthData) {
        if (loginError) {
            console.log("Login " + loginError);
        } else {
            loginData = loginAuthData;
			console.log("Authenticated successfully with payload: " + loginAuthData);
        }
    });
}