import re

# Class to parse Authorization Header
class AuthHeader:
    TOKEN_KEY = 'token='
    TOKEN_REGEX = r'^(Token|Bearer)\s+'
    AUTHN_PAIR_DELIMITERS = r'\s*(?:,|;|\t+)\s*'

    def __init__(self, auth):
        self.authorization_header = str(auth)
        token, options = self.token_and_options(self.authorization_header)
        self.token = token
        self.options = options

    def __repr__(self):
        return '%s(%r)' % (self.__class__, self.authorization_header)

    @classmethod
    def token_and_options(cls, auth):
        """Parses the token and options out of the token Authorization header."""
        """The value for the Authorization header is expected to have the prefix"""
        """<tt>"Token"</tt> or <tt>"Bearer"</tt>. If the header looks like this:"""
        """   Authorization: Token token=abc, auth_login=def"""
        """Then the returned token is <tt>abc</tt>, and the options are"""
        """<tt>{auth_login: 'def'}</tt>"""

        """auth - event['authorizationToken'] passed in from API Gateway"""
        """Returns an +Array+ of <tt>[String, Hash]</tt> if a token is present."""
        """Returns +None+ if no token is found."""
        if re.findall(cls.TOKEN_REGEX, auth):
            params = cls.token_params_from(auth)

            return [params.pop(0)[1], dict(params)]

        return [None, None]

    @classmethod
    def token_params_from(cls, auth):
        token_params = cls.rewrite_param_values(cls.params_array_from(cls.raw_params(auth)))
        return token_params

    @classmethod
    def rewrite_param_values(cls, array_params):
        """This removes the <tt>"</tt> characters wrapping the value."""
        rewrite_params = list(map(lambda x: [x[0], x[1].replace('"', '')], array_params))
        return rewrite_params

    @classmethod
    def params_array_from(cls, raw_params):
        """Takes raw_params and turns it into an array of parameters"""
        array_params = list(map(lambda x: re.split(r'=', x), raw_params))
        return array_params

    @classmethod
    def raw_params(cls, auth):
        """This method takes an authorization body and splits up the key-value"""
        """pairs by the standardized <tt>:</tt>, <tt>;</tt>, or <tt>\t</tt>"""
        """delimiters defined in +AUTHN_PAIR_DELIMITERS+."""
        _raw_params = re.split(cls.AUTHN_PAIR_DELIMITERS, re.sub(cls.TOKEN_REGEX, "", auth))
        match = re.search(r'%s' % cls.TOKEN_KEY, _raw_params[0])

        if match is None:
            _raw_params[0] = '{0}{1}'.format(cls.TOKEN_KEY, _raw_params[0])
        return _raw_params
