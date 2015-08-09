<login>
    <div>
        <input name="username" type="text" placeholder="username" />
        <input name="password" type="password" placeholder="password" />
        <button name="submit" onclick="{ submit }">
    </div>

    def submit(self, event):
        opts.login(self.username.value, self.password.value)

    @opts.on('login.success')
    def after_login_success(params):
        alert('Login success, User id: %s' % params['id'])

    @opts.on('login.fail')
    def after_login_fail(params):
        alert(params['msg'])
</login>
