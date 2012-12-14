from models import CrushHash
from Crypto.Hash import SHA512

def crush_digest(Person1, Person2):
    s1 = multi_hash(Person1.email, 2)
    s2 = multi_hash(Person2.email, 2)
    s = '%s | %s' % (s1, s2)
    s_hash = multi_hash(s, 10273)
    return s_hash

def multi_hash(string, num_iter):
    hasher = SHA512.new()
    digest = string
    for i in range(num_iter):
        hasher.update(digest)
        digest = hasher.hexdigest()
    return digest
