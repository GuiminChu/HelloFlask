from passlib.hash import pbkdf2_sha256 as sha256


class DigestUtil(object):

    @staticmethod
    def sha256(data: str) -> str:
        return sha256.hash(data)

    @staticmethod
    def verify_sha256(data, hash):
        return sha256.verify(data, hash)
