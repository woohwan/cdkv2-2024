import { handler } from "../src/services/spaces/handler";

process.env.AWS_REGION = 'ap-northeast-2';
process.env.TABLE_NAME = 'SpacesTable-02ae09b48eb2'

handler({
    httpMethod: 'POST',
    body: JSON.stringify({
        location: 'Dublin'
    })
} as any, {} as any)