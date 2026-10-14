import type { LoginType, SignupType } from "../types/signup";
import { axiosInstance } from "./axios";

export async function signup(data:SignupType){
    const result = await axiosInstance.post('/register',data)
    return result.data
}

export async function login(data:LoginType) {
 const result = await axiosInstance.post('/login',data)   
 return result.data
}


