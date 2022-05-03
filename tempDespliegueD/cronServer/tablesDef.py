user={'TableName':'usuarios',
    'KeySchema':[{'AttributeName':'id', 'KeyType':'HASH'}],
    'AttributeDefinitions':[dict(AttributeName='userId', AttributeType='S')],
    'ProvisionedThroughput':dict(ReadCapacityUnits=10, WriteCapacityUnits=10)
}

concurso={'TableName':'concursos',
    'KeySchema':[{'AttributeName':'id', 'KeyType':'HASH'}],
    'AttributeDefinitions':[dict(AttributeName='concursoId', AttributeType='S')],
    'ProvisionedThroughput':dict(ReadCapacityUnits=10, WriteCapacityUnits=10)
}

participante={'TableName':'participantes',
    'KeySchema':[{'AttributeName':'id', 'KeyType':'HASH'}],
    'AttributeDefinitions':[dict(AttributeName='participanteId', AttributeType='S')],
    'ProvisionedThroughput':dict(ReadCapacityUnits=10, WriteCapacityUnits=10)
}

models=[user,concurso,participante]