import subprocess
from crush.crush_connector.models import Person
from crush.name_lookup.views import set_user_info

def ls(dir):
    return subprocess.check_output('ls %s' % dir).split('\n')

base_dir = '/afs/athena.mit.edu/user'

def main():
    for first_letter in ls(base_dir):
        for second_letter in ls('%s/%s' % (base_dir, first_letter)):
            for athena_name in ls('%s/%s/%s' % (base_dir, first_letter, second_letter)):
                set_user_info(athena_name)

if __name__ == '__main__':
    main()
