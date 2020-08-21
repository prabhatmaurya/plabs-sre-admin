from app import app
from flask import jsonify, render_template, request
import csv
import json
from tinydb import TinyDB, Query, where
import hashlib
from lib.fabric_firewalld import VagrantClass
from lib.ansible_playbook import PlayBookJob

@app.route('/firewall/list',methods=['GET'],strict_slashes=False)
def firewall_list():
    return json.dumps(getData()['rules'])

def getData():
    db = TinyDB('rules.json')
    rich_rules_list = {}
    rich_rules_list['rules'] = db.all()
    return rich_rules_list


@app.route('/',strict_slashes=False)
def index():
    return render_template('index.html')

@app.route('/edit',methods=['GET','POST'],strict_slashes=False)
def edit():
    family = request.form['family']
    id = request.form['id']
    sourceIp = request.form['source']
    targetPort = request.form['port']
    protocol = request.form['protocol']
    state = request.form['state']

    db = TinyDB('rules.json')
    rules = Query()

    searchResult = db.search(rules.id == id)[0]
    rich_rule1 ='rule family="{0}" source address="{1}" port port="{2}" protocol="{3}" {4}'.format(searchResult['family'],searchResult['source'],searchResult['port'],searchResult['protocol'],searchResult['state'])

    isDeleted = deleteRules(rule_id=id,host_list=['192.168.10.100'],private_key_file='../ssh_key/vagrant_id_rsa',rich_rule=rich_rule1)

    if not isDeleted:
        return "400"


    md5 = hashlib.md5("%s-%s-%s-%s-%s" % (family,sourceIp,targetPort,protocol,state)).hexdigest()
    insertStatus = db.insert({
                    'id': md5,
                    'family':family,
                    'source':sourceIp,
                    'port':targetPort,
                    'protocol':protocol,
                    'state':state
    })


    playbookResponse = pb.run(host_list = ['192.168.10.100'],
                     remote_user = 'vagrant',
                     private_key_file='../ssh_key/vagrant_id_rsa',
                     rich_rule ='rule family="{0}" source address="{1}" port port="{2}" protocol="{3}" {4}'.format(family,sourceIp,targetPort,protocol,state),
                     state = 'enabled'
         )


    return "200"

@app.route('/insert',methods=['GET','POST'],strict_slashes=False)
def insert():
    family = request.form['family']
    sourceIp = request.form['source']
    targetPort = request.form['port']
    protocol = request.form['protocol']
    state = request.form['state']

    db = TinyDB('rules.json')
    rules = Query()
    # pb = PlayBookJob()
    # playbookResponse = pb.run(host_list = ['192.168.10.100'],
    #                  remote_user = 'vagrant',
    #                  private_key_file='../ssh_key/vagrant_id_rsa',
    #                  rich_rule ='rule family="{0}" source address="{1}" port port="{2}" protocol="{3}" {4}'.format(family,sourceIp,targetPort,protocol,state),
    #                  state = 'enabled'
    #      )
    obj = VagrantClass(vagrantfile='/Users/prabhat.maurya/Documents/GIT/plabs/python/plabs-python-flask/')
    rich_rule ='rule family="{0}" source address="{1}" port port="{2}" protocol="{3}" {4}'.format(family,sourceIp,targetPort,protocol,state)
    response = []
    playbookResponse = obj.insert_rules(machine_name='flask',rule=rich_rule)
    for host in playbookResponse:
            #if playbookResponse[host]['changed']:
            if playbookResponse[host]:
                md5 = hashlib.md5("%s-%s-%s-%s-%s" % (family,sourceIp,targetPort,protocol,state)).hexdigest()
                insertStatus = db.insert({
                                'id': md5,
                                'family':family,
                                'source':sourceIp,
                                'port':targetPort,
                                'protocol':protocol,
                                'state':state,
                                'host':'192.168.10.100'
                        })
                if insertStatus:
                    response.append(dict(status=200,msg="Data Insert Success",host=host))
                else:
                    response.append(dict(status=400,msg="DB Insert Failed",host=host))
            else:
                response.append(dict(status=200,msg="Failed to update firewall rule",host=host))
    return json.dumps(response)

@app.route('/delete',methods=['GET','POST'],strict_slashes=False)
def delete():
    family = request.form['family']
    id = request.form['id']
    sourceIp = request.form['source']
    targetPort = request.form['port']
    protocol = request.form['protocol']
    state = request.form['state']

    db = TinyDB('rules.json')
    rules = Query()

    searchResult = db.search(rules.id == id)[0]
    rich_rule1 ='rule family="{0}" source address="{1}" port port="{2}" protocol="{3}" {4}'.format(searchResult['family'],searchResult['source'],searchResult['port'],searchResult['protocol'],searchResult['state'])

    isDeleted = deleteRules(rule_id=id,host_list=['192.168.10.100'],private_key_file='../ssh_key/vagrant_id_rsa',rich_rule=rich_rule1)

    if not isDeleted:
        return "400"
    else:
        return "200"


def insertRules(rule_id,host_list,private_key_file,rich_rule,machine_name):
    db = TinyDB('rules.json')
    obj = VagrantClass(vagrantfile='/Users/prabhat.maurya/Documents/GIT/plabs/python/plabs-python-flask/')
    playbookResponse = obj.insert_rules(machine_name=machine_name,rule=rich_rule)
    for host in playbookResponse:
            #if playbookResponse[host]['changed']:
            if playbookResponse[host]:
                md5 = rule_id
                insertStatus = db.insert({
                                'id': md5,
                                'family':family,
                                'source':sourceIp,
                                'port':targetPort,
                                'protocol':protocol,
                                'state':state,
                                'host':'192.168.10.100'
                        })
                return insertStatus
            else:
                return "400"

def deleteRules(rule_id,host_list,private_key_file,rich_rule):
    db = TinyDB('rules.json')
    #rules = Query()
    searchResult = db.search(Query().id == rule_id)[0]
    # pb = PlayBookJob()
    # playbookResponse = pb.run(host_list = host_list,
    #                  remote_user = 'vagrant',
    #                  private_key_file='../ssh_key/vagrant_id_rsa',
    #                  rich_rule ='rule family="{0}" source address="{1}" port port="{2}" protocol="{3}" {4}'.format(searchResult['family'],searchResult['source'],searchResult['port'],searchResult['protocol'],searchResult['state']),
    #                  state = 'disabled'
    #      )
    obj = VagrantClass(vagrantfile='/Users/prabhat.maurya/Documents/GIT/plabs/python/plabs-python-flask/')
    rich_rule ='rule family="{0}" source address="{1}" port port="{2}" protocol="{3}" {4}'.format(searchResult['family'],searchResult['source'],searchResult['port'],searchResult['protocol'],searchResult['state'])
    playbookResponse = obj.delete_rules(machine_name='flask',rule=rich_rule)
    print rich_rule
    print playbookResponse
    for host in playbookResponse:
        #if playbookResponse[host]['changed']:
        print playbookResponse[host]
        if playbookResponse[host] == 'success':
            deleteStatus = db.remove(Query().id == rule_id)
            print rule_id
            return deleteStatus
        else:
            return False

@app.route('/reloaddb',strict_slashes=False)
def reload_db():
    response = []
    db = TinyDB('rules.json')
    obj = VagrantClass(vagrantfile='/Users/prabhat.maurya/Documents/GIT/plabs/python/plabs-python-flask/')

    rules_list = obj.fetch_rules(machine_name='flask')
    for host in rules_list:
        for rules in rules_list[host]:
            family = rules['family']
            sourceIp = rules['sourceIp']
            targetPort = rules['targetPort']
            protocol = rules['protocol']
            state = rules['state']
            md5 = rules['md5']
            host = host

            ## For empty table
            if db.search(Query().id.exists()):
                ## Check Duplicate record
                ifExists = db.search(Query().id == md5)
            else:
                ifExists = []

            ## if no duplicate found then insert data
            if len(ifExists) == 0:
                status = db.insert({
                                'id': md5,
                                'family':family,
                                'source':sourceIp,
                                'port':targetPort,
                                'protocol':protocol,
                                'state':state,
                                'host':host
                })
                if status:
                    status_dict = dict(request=sourceIp,message="Successfully inserted record for: %s" % sourceIp,status=200)
                    response.append(status_dict)
                else:
                    status_dict = dict(request=sourceIp,message="Failed inserted record for: %s" % sourceIp,status=400)
                    response.append(status_dict)
            else:
                status_dict = dict(request=sourceIp,message="Duplicate record for: %s" % sourceIp,status=201)
                response.append(status_dict)
        return json.dumps(response)

@app.route('/fetch',strict_slashes=False)
def fetch():

    db = TinyDB('rules.json')
    ## Clean DB
    db.purge()
    with open('input.txt') as f:
        rd = csv.reader(f,delimiter=" ")
        for row in rd:
            if(len(row) == 8):
                family = row[1].split('=')[1].strip('"')
                sourceIp = row[3].split('=')[1].strip('"')
                targetPort = row[5].split('=')[1].strip('"')
                protocol = row[6].split('=')[1].strip('"')
                state = row[7]
            elif(len(row) == 5):
                family = row[1].split('=')[1].strip('"')
                sourceIp = row[3].split('=')[1].strip('"')
                targetPort = 'All'
                protocol = 'Both'
                state = row[4]
            md5 = hashlib.md5("%s-%s-%s-%s-%s" % (family,sourceIp,targetPort,protocol,state)).hexdigest()
            rules = Query()
            ifExists = db.search(rules.id == md5)
            if len(ifExists) == 0:
                status = db.insert({
                                'id': md5,
                                'family':family,
                                'source':sourceIp,
                                'port':targetPort,
                                'protocol':protocol,
                                'state':state
                })
                if status:
                    response = "200"
                else:
                    response = "400"
            else:
                response = "201"

    return response



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5010,debug=True)
