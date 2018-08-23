pragma solidity ^0.4.21;

contract NameValue2 {
    uint[] public keys;
    struct ValueStruct {
        string value;
        string author;
        uint updated_date;
    }
    mapping (uint => ValueStruct) public data;

    event KeyUpdated(string key, string value, string author, uint updated_date);
    event KeyRemoved(string key, string value, string author, uint updated_date);

    function update(string key, string value, string author) public {
        uint key_uint = stringToUintHash(key);
        uint updated_date = now;

        data[key_uint] = ValueStruct(value, author, updated_date);

        bool exists = false;
        for (uint i=0; i<keys.length; i++) {
            if (keys[i] == key_uint) {
                exists = true;
                break;
            }
        }

        if (! exists) {
            keys.push(key_uint);
        }

        emit KeyUpdated(key, value, author, updated_date);
    }

    function stringToUintHash(string str) private pure returns (uint) {
        bytes memory tempEmptyStringTest = bytes(str);
        if (tempEmptyStringTest.length == 0) {
            return 0;
        }

        bytes32 b;
        assembly {
            b := mload(add(str, 32))
        }

        return uint(b);
    }

    function get(string key) public view returns (string, string, uint) {
        uint key_uint = stringToUintHash(key);
        return (data[key_uint].value, data[key_uint].author, data[key_uint].updated_date);
    }

    function remove(string key) public {
        uint key_uint = stringToUintHash(key);

        emit KeyRemoved(key, data[key_uint].value, data[key_uint].author, data[key_uint].updated_date);

        delete data[key_uint];
        uint deleteIndex;
        for (uint i=0; i<keys.length; i++) {
            if (keys[i] == key_uint) {
                deleteIndex = i;
                break;
            }
        }

        for (i = deleteIndex; i<keys.length-1; i++){
            keys[i] = keys[i+1];
        }
        keys.length--;

    }

    function dumpKeys() public view returns (uint[]){
        return keys;
    }
}
