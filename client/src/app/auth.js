import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

export const {
    handlers: { GET, POST },
    auth
} = NextAuth({
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_ID,
            clientSecret: process.env.GOOGLE_SECRET
        })
    ],
    pages: {
        signIn: '/sign-in'
    }
});