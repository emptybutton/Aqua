const isReplicaSetCreated = () => {
    try {
        rs.status();
        return true
    } catch {
        return false;
    }
}

const createReplicaSet = () => rs.initiate({
    _id: "aquaSet",
    members: [
        {_id: 1, host: "aqua-mongo1"},
        {_id: 2, host: "aqua-mongo2"},
        {_id: 3, host: "aqua-mongo3"},
    ]
})

if (!isReplicaSetCreated())
    console.log(createReplicaSet());
else
    console.log(rs.status());
