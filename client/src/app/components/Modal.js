"use client";

import React, { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { Divider, Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Card, CardHeader, CardBody, Image, Input } from "@nextui-org/react";

export default function UserPicker({ searchParams }) {
    const { isOpen, onOpen, onOpenChange } = useDisclosure();
    const [userType, setUserType] = useState("none");
    const { data: session, status } = useSession()
    const [grade, setGrade] = useState(1);
    const [childName, setChildName] = useState("");
    const [childAge, setChildAge] = useState(1);
    const [instructorID, setInstructorID] = useState(0);
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const router = useRouter();

    useEffect(() => {
        if (status === "authenticated") {
            const userExists = fetch(`http://localhost:3500/user/${session.user.email}`).then((res) => res.json()).then((data) => data !== null).then((data) => {
                if (searchParams["new"] === "1" && !data) {
                    // if (searchParams["new"] === "1") {
                    //     onOpen();
                    // }
                    onOpen();
                }
                else if (searchParams["new"] === "1" && data) {
                    fetch(`http://localhost:3500/user/${session.user.email}`).then((res) => res.json()).then((data) => {
                        if (data['type'] === "instructor") {
                            setUserType("instructor");
                        } else {
                            setUserType("parent");
                        }
                    });
                }
            });
        }
    }, [searchParams]);

    useEffect(() => {
        if (status === "authenticated" && !name && !email) {
            setName(session.user.name);
            setEmail(session.user.email);
        }
    }, [status]);

    useEffect(() => {
        router.refresh();
    }, []);

    const submitInstructor = () => {
        console.log("Test ", name, email, grade);
        const instructor = fetch(`http://localhost:3500/instructor`, {
            method: "POST", body: JSON.stringify({
                name: name,
                email: email,
                grade: grade
            }),
            headers: {
                "Content-Type": "application/json"
            }
        }).then((res) => res.json()).then((data) => console.log(data));
    };

    const submitParent = () => {
        console.log("Test ", name, email, childName, childAge, instructorID);
        const parent = fetch(`http://localhost:3500/parent`, {
            method: "POST", body: JSON.stringify({
                name: name,
                email: email,
                child_name: childName,
                child_age: childAge,
                instructor_id: instructorID
            }), headers: {
                "Content-Type": "application/json"
            }
        }).then((res) => res.json()).then((data) => console.log(data));
    }

    return (
        <>
            <Modal isOpen={isOpen} onOpenChange={onOpenChange} size="2xl" isDismissable={false} hideCloseButton={true}>
                <ModalContent>
                    {(onClose) => (
                        <>
                            <ModalHeader className="flex flex-col gap-1">Are you a instructor or parent?</ModalHeader>
                            {userType === "none" ? <div>
                                <ModalBody>
                                    <div className="flex h-auto items-center space-x-4 text-small justify-center">
                                        <Card className="py-4 flex" isPressable onPress={() => setUserType("instructor")}>
                                            <CardHeader className="pb-0 pt-2 px-4 flex-col items-center">
                                                <h1 className="font-bold text-large">Instructor</h1>
                                            </CardHeader>
                                            <CardBody className="overflow-visible py-2">
                                                <Image
                                                    alt="Card background"
                                                    className="object-contain rounded-xl h-40"
                                                    src="/instructor.png"
                                                    width={270}
                                                />
                                            </CardBody>
                                        </Card>
                                        <Divider orientation="vertical" />
                                        <Card className="py-4 flex" isPressable onPress={() => setUserType("parent")}>
                                            <CardHeader className="pb-0 pt-2 px-4 flex-col items-center">
                                                <h1 className="font-bold text-large">Parent</h1>
                                            </CardHeader>
                                            <CardBody className="overflow-visible py-2">
                                                <Image
                                                    alt="Card background"
                                                    className="object-contain rounded-xl h-40"
                                                    src="/parents.png"
                                                    width={270}
                                                />
                                            </CardBody>
                                        </Card>
                                    </div>
                                </ModalBody>
                            </div> : userType === "instructor" ? <div>
                                <ModalBody>
                                    <div className="flex h-auto items-center space-x-4 text-small justify-center">
                                        <h1 className="font-bold text-large">Instructor</h1>
                                        <Input type="number" label="Grade" value={grade} onValueChange={setGrade} />
                                    </div>
                                </ModalBody>
                                <ModalFooter>
                                    <Button color="primary" onPress={() => { submitInstructor(); onClose(); router.replace('/', undefined, { shallow: true }); }}>
                                        Submit
                                    </Button>
                                </ModalFooter>
                            </div> : <div>
                                <ModalBody>
                                    <div className="flex h-auto items-center space-x-4 text-small justify-center">
                                        <h1 className="font-bold text-large">Parent</h1>
                                        <Input type="text" label="Child's Name" value={childName} onValueChange={setChildName} />
                                        <Input type="number" label="Child's Age" value={childAge} onValueChange={setChildAge} />
                                        <Input type="number" label="Instructor ID" value={instructorID} onValueChange={setInstructorID} />
                                    </div>
                                </ModalBody>
                                <ModalFooter>
                                    <Button color="primary" onPress={() => { submitParent(); onClose(); router.replace('/', undefined, { shallow: true }); }}>
                                        Submit
                                    </Button>
                                </ModalFooter>
                            </div>
                            }
                        </>
                    )}
                </ModalContent>
            </Modal>
        </>
    );
}
