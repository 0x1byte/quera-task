"use client";
import { Toaster, toaster } from "@/components/ui/toaster";
import { Container } from "@chakra-ui/react";
import { Flex, Text, Card, Stack, Input, Button } from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { userExists } from "@/utils/requests";

export default function Home() {
  const [username, setUsername] = useState("");
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const status = await userExists(username);
      if (status === 200) {
        router.push(`/profile/${username}`);
      }
    } catch (error) {
      if (error.response.status === 404) {
        toaster.create({
          title: "User not found",
          status: "error",
          duration: 5000,
        });
      } else {
        toaster.create({
          title: "Something went wrong",
          status: "error",
          duration: 5000,
        });
      }
    }
  };

  return (
    <Container>
      <Flex h="100vh" justifyContent="center" alignItems="center">
        <Card.Root width="md">
          <Card.Header>
            <Card.Title>
              <Text fontSize="3xl">Github User Search</Text>
            </Card.Title>
            <Card.Description>
              Search any github user and get their details
            </Card.Description>
          </Card.Header>
          <Card.Body>
            <Stack gap="4" w="full">
              <Field label="Username">
                <Input
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </Field>
            </Stack>
          </Card.Body>
          <Card.Footer>
            <Button
              type="submit"
              onClick={handleSubmit}
              variant="solid"
              size="md"
            >
              Search
            </Button>
          </Card.Footer>
        </Card.Root>
      </Flex>
      <Toaster />
    </Container>
  );
}
