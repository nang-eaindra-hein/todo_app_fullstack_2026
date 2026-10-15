export enum TodoStatusEnum {
  Todo = "Todo",
  InProgress = "In_Progress",
  Done = "Done",
}

export interface createListType{
    title: string
    description: string
    status: TodoStatusEnum

}

export interface updateStatusType{
    status: TodoStatusEnum
    id:string

}

export interface updateListType{
    id:number
    title: string
    description: string
    status: TodoStatusEnum
}

export type TodoStatus = (typeof TodoStatusEnum)[keyof typeof TodoStatusEnum];
